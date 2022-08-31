#!/usr/bin/env python3
import prisma_settings
import csv
from csv import DictReader
from files.pa_api_calls import *


# Global Vars
SCRIPT_NAME = 'Prisma Access: Remote Networks'
SCRIPT_VERSION = "1"


####################################################################
# Read cloudgenix_settings file for auth token or username/password
####################################################################

try:
    from prisma_settings import TSG_ID
    from prisma_settings import CLIENT_ID
    from prisma_settings import CLIENT_SECRET

except ImportError:
    TSG_ID = None
    CLIENT_ID = None
    CLIENT_SECRET = None

def create_remote_networks(list_from_csv, token):
    
    for network in list_from_csv:
        
        print("\nWorking on " + network["remote_network_name"] + "\n")
        
        if not ike_gateway(network, token):
            print("\nSkipping " + network["remote_network_name"] + " due to an error\n")
            continue
        if not ipsec_tunnel(network, token):
            print("\nSkipping " + network["remote_network_name"] + " due to an error\n")
            continue
        if not remote_network(network, token):
            print("\nSkipping " + network["remote_network_name"] + " due to an error\n")
            continue 
    
    print("\nCompleted all Remote Networks\n")       
            
    return

def ike_gateway(network, token):
    success = False
    data = {"authentication": {"pre_shared_key": {"key": network["pre_shared_key"]}}, "local_id": {'type': 'ufqdn', 'id': network["local_fqdn"]}, "name": "ike_GW_" + network["remote_network_name"], "peer_address": {'dynamic': {}}, "peer_id": {'type': 'ufqdn', 'id': network["peer_fqdn"]}, 'protocol_common': {'nat_traversal': {'enable': True}, 'fragmentation': {'enable': False}}, 'protocol': {'ikev1': {'ike_crypto_profile': network["ike_crypto_profile"], 'dpd': {'enable': True}}, 'ikev2': {'ike_crypto_profile': network["ike_crypto_profile"], 'dpd': {'enable': True}}, 'version': 'ikev2-preferred'}, "protocol_common": {"fragmentation": {"enable": False},"nat_traversal": {"enable": True},"passive_mode": True}}
    ike_gateway = False
    for item in sase_get_remote_networks_ike_gateways(token):
        if item["name"] == "ike_GW_" + network["remote_network_name"]:
            ike_gateway = True
            id = item["id"]            
            continue
    
    if ike_gateway == False:
        response, error = sase_post_remote_networks_ike_gateways(token, data)
        if response:
            print("Creating IKE Gateway " + "ike_GW_" + network["remote_network_name"])
            success = True
        else:
            print("Error creating IKE Gateway " + "ike_GW_" + network["remote_network_name"])
            print(error)
    else:
        response, error = sase_put_remote_networks_ike_gateways(token, data, id)
        if response:
            print("Updating IKE Gateway " + "ike_GW_" + network["remote_network_name"])
            success = True
        else:
            print("Error updating IKE Gateway " + "ike_GW_" + network["remote_network_name"])
            print(error)
    return success

def ipsec_tunnel(network, token):
    success = False
    data = {"anti_replay": True, "auto_key": { "ike_gateway": [{"name":"ike_GW_" + network["remote_network_name"]} ] , "ipsec_crypto_profile": network["ipsec_crypto_profile"]}, "copy_tos": False, "enable_gre_encapsulation": False, "name": "ipsec_tunnel_" + network["remote_network_name"]}
    
    if network["tunnel_monitor"] == "TRUE":
        data["tunnel_monitor"] = {"destination_ip": network["monitor_ip"], "enable": True}
   
    ipsec_tunnel = False
    for item in sase_get_remote_networks_ipsec_tunnels(token):
        if item["name"] == "ipsec_tunnel_" + network["remote_network_name"]:
            ipsec_tunnel = True
            id = item["id"]            
            continue
    
    if ipsec_tunnel == False:
        response, error = sase_post_remote_networks_ipsec_tunnels(token, data)
        if response:
            print("Creating IPSec Tunnel " + "ipsec_tunnel_" + network["remote_network_name"])
            success = True
        else:
            print("Error creating IPSec Tunnel " + "ipsec_tunnel_" + network["remote_network_name"])
            print(error)
    else:
        response, error = sase_put_remote_networks_ipsec_tunnels(token, data, id)
        if response:
            print("Updating IPSec Tunnel " + "ipsec_tunnel_" + network["remote_network_name"])
            success = True
        else:
            print("Error updating IPSec Tunnel " + "ipsec_tunnel_" + network["remote_network_name"])
            print(error)
    return success

def remote_network(network, token):
    success = False
    data = { "ipsec_tunnel": "ipsec_tunnel_" + network["remote_network_name"], "license_type": "FWAAS-AGGREGATE", "name": network["remote_network_name"], "region": network["region"], "spn_name": network["spn_name"]}
    if network["static_enabled"] == "TRUE":
        static_string = network["static_routing"].replace(" ", "")
        static_list = list(static_string.split(","))
        data["subnets"] = static_list
    if network["bgp_enabled"] == "TRUE":
        data["protocol"] = {"bgp": {"do_not_export_routes": False,"enable": True,"local_ip_address": network["bgp_local_ip"],"originate_default_route": True,"peer_as": network["bgp_peer_as"],"peer_ip_address": network["bgp_peer_ip"],"peering_type": "exchange-v4-over-v4","summarize_mobile_user_routes": True},"bgp_peer": {"local_ip_address": network["bgp_local_ip"],"peer_ip_address": network["bgp_peer_ip"]}}
         
    remote_network = False
    for item in sase_get_remote_networks(token):
        if item["name"] == network["remote_network_name"]:
            remote_network = True
            id = item["id"]            
            continue
    
    if remote_network == False:
        response, error = sase_post_remote_networks(token, data)
        if response:
            print("Creating Remote Network " + network["remote_network_name"])
            success = True
        else:
            print("Error creating Remote Network " + network["remote_network_name"])
    else:
        response, error = sase_put_remote_networks(token, data, id)
        if response:
            print("Updating Remote Network " + network["remote_network_name"])
            success = True
        else:
            print("Error updating Remote Network " + network["remote_network_name"])
    return success
                                          
def go():
    ############################################################################
    # Begin Script, parse arguments.
    ############################################################################
    token = prisma_access_auth(TSG_ID, CLIENT_ID, CLIENT_SECRET)
    sase_get_bandwidth_allocations(token)    
    try:
        with open("remote_networks.csv", "r") as csvfile:
            csvreader = DictReader(csvfile)
            list_from_csv = []
            for row in csvreader:
                list_from_csv.append(row)
    except:
        print("Error importing CSV")
        return
    create_remote_networks(list_from_csv, token)
    return

if __name__ == "__main__":
    go()
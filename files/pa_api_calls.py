#!/usr/bin/env python3
import requests
from requests_toolbelt.utils import dump

def prisma_access_auth(TSG_ID, CLIENT_ID, CLIENT_SECRET):
    token = None
    
    url = "https://auth.apps.paloaltonetworks.com/oauth2/access_token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded',}
    data = 'grant_type=client_credentials&scope=tsg_id:' + TSG_ID
    auth = (CLIENT_ID, CLIENT_SECRET)

    response = requests.post(url=url, headers=headers, data=data, auth=auth)
    if response:
        response = response.json()
        token = response["access_token"]
    else:
        print("Print failed to generate auth token")
    
    return token


def sase_get_bandwidth_allocations(token):
    url = "https://api.sase.paloaltonetworks.com/sse/config/v1/bandwidth-allocations"
    headers = {"authorization": f"Bearer {token}", "content-type": "application/json"}

    response = requests.get(url=url, headers=headers)
    if response:
        response = response.json()
    else:
        print("Print failed getting remote network bandwidth allocation")
        response = None
    return response

def sase_get_remote_networks_ike_crypto_profiles(token):
    url = "https://api.sase.paloaltonetworks.com/sse/config/v1/ike-crypto-profiles"
    headers = {"authorization": f"Bearer {token}", "content-type": "application/json"}
    params = {"folder":"Remote Networks"}

    response = requests.get(url=url, headers=headers, params=params)
    if response:
        response = response.json()
        response = response["data"]
    else:
        print("Print failed to get remote network ike crypto profiles")
        response = None
    return response
    
def sase_get_remote_networks_ike_gateways(token):
    url = "https://api.sase.paloaltonetworks.com/sse/config/v1/ike-gateways"
    headers = {"authorization": f"Bearer {token}", "content-type": "application/json"}
    params = {"folder":"Remote Networks"}

    response = requests.get(url=url, headers=headers, params=params)
    if response:
        response = response.json()
        response = response["data"]
    else:
        print("Print failed to get remote network ike gateways")
        response = None
    return response

def sase_get_remote_networks_ipsec_crypto_profiles(token):
    url = "https://api.sase.paloaltonetworks.com/sse/config/v1/ipsec-crypto-profiles"
    headers = {"authorization": f"Bearer {token}", "content-type": "application/json"}
    params = {"folder":"Remote Networks"}

    response = requests.get(url=url, headers=headers, params=params)
    if response:
        response = response.json()
        response = response["data"]
    else:
        print("Print failed to get remote network ipsec crypto profiles")
        response = None
    return response

def sase_get_remote_networks_ipsec_tunnels(token):
    url = "https://api.sase.paloaltonetworks.com/sse/config/v1/ipsec-tunnels"
    headers = {"authorization": f"Bearer {token}", "content-type": "application/json"}
    params = {"folder":"Remote Networks"}

    response = requests.get(url=url, headers=headers, params=params)
    if response:
        response = response.json()
        response = response["data"]
    else:
        print("Print failed to get remote network ipsec tunnels")
        response = None
    return response

def sase_get_remote_networks(token):
    url = "https://api.sase.paloaltonetworks.com/sse/config/v1/remote-networks"
    headers = {"authorization": f"Bearer {token}", "content-type": "application/json"}
    params = {"folder":"Remote Networks"}

    response = requests.get(url=url, headers=headers, params=params)
    if response:
        response = response.json()
        response = response["data"]
    else:
        print("Print failed to get remote network")
        response = None
    return response

def sase_post_remote_networks_ike_gateways(token, data):
    url = "https://api.sase.paloaltonetworks.com/sse/config/v1/ike-gateways"
    headers = {"authorization": f"Bearer {token}", "content-type": "application/json"}
    params = {"folder":"Remote Networks"}
    
    response = requests.post(url=url, headers=headers, json=data, params=params)
    if response:
        response = response
        error = None
    else:
        print("Print failed to create remote network ike gateways")
        data = dump.dump_all(response)
        error = data.decode('utf-8')
        response = None
    return response, error

def sase_post_remote_networks_ipsec_tunnels(token, data):
    url = "https://api.sase.paloaltonetworks.com/sse/config/v1/ipsec-tunnels"
    headers = {"authorization": f"Bearer {token}", "content-type": "application/json"}
    params = {"folder":"Remote Networks"}
    
    response = requests.post(url=url, headers=headers, json=data, params=params)
    if response:
        response = response
        error = None
    else:
        print("Print failed to create remote network ipsec tunnels")
        data = dump.dump_all(response)
        error = data.decode('utf-8')
    return response, error

def sase_post_remote_networks(token, data):
    url = "https://api.sase.paloaltonetworks.com/sse/config/v1/remote-networks"
    headers = {"authorization": f"Bearer {token}", "content-type": "application/json"}
    params = {"folder":"Remote Networks"}
    
    response = requests.post(url=url, headers=headers, json=data, params=params)
    if response:
        response = response
        error = None
    else:
        print("Print failed to create remote network")
        data = dump.dump_all(response)
        error = data.decode('utf-8')
    return response, error

def sase_put_remote_networks_ike_gateways(token, data, id):
    url = "https://api.sase.paloaltonetworks.com/sse/config/v1/ike-gateways/" + id
    headers = {"authorization": f"Bearer {token}", "content-type": "application/json"}
    params = {"folder":"Remote Networks"}
    
    response = requests.put(url=url, headers=headers, json=data, params=params)
    if response:
        response = response
        error = None
    else:
        print("Print failed to create remote network ike gateways")
        data = dump.dump_all(response)
        error = data.decode('utf-8')
        response = None
    return response, error

def sase_put_remote_networks_ipsec_tunnels(token, data, id):
    url = "https://api.sase.paloaltonetworks.com/sse/config/v1/ipsec-tunnels/" + id
    headers = {"authorization": f"Bearer {token}", "content-type": "application/json"}
    params = {"folder":"Remote Networks"}
    
    response = requests.put(url=url, headers=headers, json=data, params=params)
    if response:
        response = response
        error = None
    else:
        print("Print failed to create remote network ipsec tunnels")
        data = dump.dump_all(response)
        error = data.decode('utf-8')
        response = None
    return response, error
    
def sase_put_remote_networks(token, data, id):  
    url = "https://api.sase.paloaltonetworks.com/sse/config/v1/remote-networks/" + id
    headers = {"authorization": f"Bearer {token}", "content-type": "application/json"}
    params = {"folder":"Remote Networks"}
    
    response = requests.put(url=url, headers=headers, json=data, params=params)
    if response:
        response = response
        error = None
    else:
        print("Print failed to create remote network ipsec tunnels")
        data = dump.dump_all(response)
        error = data.decode('utf-8')
        response = None
    return response, error
# Prisma Access Cloud Manager Bulk Remote Networks (Preview)
The purpose of this script is to bulk import Remote Networks into Cloud Manager from a CSV

#### License
MIT

#### Requirements
* Active Prisma Access with API Gateway and Remote Network Bandwidth
* Python >=3.7

#### Installation:
 Scripts directory. 
 - **Github:** Download files to a local directory, manually run the scripts. 
 - pip install -r requirements.txt
 
### Examples of usage:
 Please generate your TSG ID, Client ID and Client Secret then add them to prisma_settings.py file
 Please update the remote_networks.csv with all the Remote Networks you want to build 
 
 - ./remote-networks.py -F remote_networks.csv 
 
 This script does not commit the changes. That must be done from the portal. 
 
### Caveats and known issues:
 - This is a PREVIEW release, hiccups to be expected. Please file issues on Github for any problems.
 - This does not support ECMP
 - ike_crypto_profiles and ipsec_cyrpto_profiles must be configured in the portal
 - Certain BGP settings are hard coded but can be changed in the script
 - IKE identification is set to User FQDN 

#### Version
| Version | Build | Changes |
| ------- | ----- | ------- |
| **1.0.0** | **b1** | Initial Release. |


#### For more info
 * Get help and additional Prisma Access Documentation at <https://pan.dev/sase/>

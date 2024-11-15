from pysnmp.hlapi import *
from ipaddress import ip_address
from googleapiclient.discovery import build
import json
import secrets  # For secure password storage (optional)
import google_sheets_functions as gsf

with open(
    'api_accounts.json',
    'r') as api_accounts:
    api_keys = json.load(api_accounts)
google_api_info = api_keys['google'][0]


# SNMP details
host = "10.111.111.2"  # Replace with your switch's IP address
# input_host = input(f"Enter target IP address (Default={host})")
# if input_host == '':
#     input_host = host
# print(f'input_host={input_host}')
community = "testGroup"
oid = "1.3.6.1.2.1.17.4.3.1.2"  # D-Link MIB for MAC address table

# Google Sheet details
spreadsheet_id = "1w_Ro8l1HVdPSVGqMw1ujzuCaXTobHPKbA9LdFp_y5JY"
sheet_name = "Sheet1"

from pysnmp.hlapi import *

# Replace with actual values (obtain securely)
auth_username = "your_valid_snmpv3_auth_username"
auth_protocol = AuthProtocol.HMAC_SHA  # Adjust based on SNMPv3 configuration
auth_passphrase = "your_strong_snmpv3_auth_passphrase"
priv_protocol = PrivProtocol.DES  # Adjust based on SNMPv3 configuration
priv_passphrase = "your_strong_snmpv3_priv_passphrase"

# Construct the SNMP v3 authentication and privacy context
auth_data = CommunityData(community)  # Switch to AuthData with proper credentials for SNMPv3
context = ContextData()

# Build the SNMP request
errorIndication, errorStatus, errorIndex, varBinds = next(
    bulkCmd(SnmpEngine(),
            auth_data,
            UdpTransportTarget((host, 161)),
            context,
            0, 25,
            ObjectType(ObjectIdentity(oid))
            )
)

# Parse and process the response
if errorIndication:
    print(f"Error: {errorIndication}")
elif errorStatus:
    print(f"[Level {errorStatus[0]} & Status {errorStatus[1][0]} on {errorStatus[1][1]}] {errorStatus[0]}")
else:
    for varBind in varBinds:
        # Extract and process retrieved data from varBind here
        print(f"{varBind[0].prettyPrint()}: {varBind[1].prettyPrint()}")

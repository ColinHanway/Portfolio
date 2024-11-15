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

# Function to parse MAC address entry
def parse_mac_entry(varBind):
    port = varBind[0].prettyPrint()[-1:]
    mac = varBind[1].prettyPrint()[-17:]
    vid = varBind[2].prettyPrint()[-1:]
    return f"{port},{mac},{vid}"

# Connect to SNMP agent
errorIndication, errorStatus, errorIndex, varBindTable = next(
    bulkCmd(SnmpEngine(), CommunityData(community), UdpTransportTarget((host, 161)), ContextData(), 0, 25, ObjectType(ObjectIdentity(oid)))
)

# Extract MAC addresses and build list
mac_list = []
for varBind in varBindTable:
    for varBinds in varBinds:
        mac_list.append(parse_mac_entry(varBinds))


# Clear existing data and insert new rows
body = {
    "values": [["Port", "MAC Address", "VID"]] + [[entry.split(",") for entry in mac_list]]
}
print(body)

# google_sheet_id = '1w_Ro8l1HVdPSVGqMw1ujzuCaXTobHPKbA9LdFp_y5JY'
# google_sheet_name = 'Sheet1'
# google_sheet_range = f'{google_sheet_name}!$A$1:$R'
# google_sheet_range_date_updated = f'{google_sheet_name}!$C$1:$D$2'

# # CLEAR SHEET
# if gsf.clear_sheet(spreadsheetId=google_sheet_id, range=google_sheet_range, api=google_api_info):
#     print('Successfully cleared sheet')
# else:
#     print("An error occurred attempting to clear the Google Sheet")

# # WRITE MAC TABLE TO SHEET
# if gsf.append_sheet(spreadsheetId=google_sheet_id, range=google_sheet_range, body=body, api=google_api_info):
#     print('Successfully wrote to sheet')
# else:
#     print("An error occurred attempting to write data to the Google Sheet")

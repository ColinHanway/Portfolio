### GLOBAL IMPORTS ###
import sys, os
from urllib.parse import urlencode
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###
import base64
from email.utils import formatdate
import hashlib
import hmac
import requests
import pandas as pd

### GLOBAL VARIABLES ###
api_name = 'ninjaone (legacy)'
auth_url = "https://app.ninjarmm.com/ws/oauth/token" 
API_URL = "https://app.ninjarmm.com"
USERS_PATH = "/v2/users"
CUSTOMERS_PATH = "/v1/customers"
DEVICES_PATH = "/v2/devices"
ORGANIZATIONS_PATH = "/v2/organizations"
LOCATIONS_PATH = "/v2/locations"
ROLES_PATH = "/v1/technicians"

class Organization:
    def __init__(self, data):
        self.location_id = data.get('id')
        self.location_name = data.get('name')
        self.node_approval_mode = data.get('nodeApprovalMode')

    def to_list(self):
        """ Convert the location object to a list of its attributes """
        return [
            self.location_id,
            self.location_name,
            self.node_approval_mode
        ]
        
class Location:
    def __init__(self, data):
        self.location_id = data.get('id')
        self.location_name = data.get('name')
        self.location_organizationId = data.get('organizationId')
        self.location_description = data.get('description')
        self.location_address = data.get('address')

    def to_list(self):
        """ Convert the location object to a list of its attributes """
        return [
            self.location_id,
            self.location_name,
            self.location_organizationId,
            self.location_description,
            self.location_address
        ]
        
class User:
    def __init__(self, user_dict):
        self.user_dict = user_dict
        self.user_id = self.user_dict["administrator"]
        self.user_invitationStatus = self.user_dict["invitationStatus"]
        self.user_mfaConfigured = self.user_dict["mfaConfigured"]
        self.user_mustChangePw = self.user_dict["mustChangePw"]
        self.user_notifyAllClients = self.user_dict["notifyAllClients"]
        self.user_organizationId = self.user_dict["organizationId"]
        self.user_permitAllClients = self.user_dict["permitAllClients"]
        self.user_phone = self.user_dict["phone"]
        self.user_administrator = self.user_dict["administrator"]
        self.user_deviceIds = self.user_dict["deviceIds"]
        self.user_email = self.user_dict["email"]
        self.user_enabled = [self.user_dict["enabled"]]
        self.user_fields = self.user_dict["fields"]
        self.user_firstName = self.user_dict["firstName"]
        self.user_lastName = self.user_dict["lastName"]
        self.user_tags = self.user_dict["tags"]
        self.user_userType = self.user_dict["userType"]

class Device:
    def __init__(self, data):
        self.approval_status = data.get('approvalStatus')
        self.created = format_timestamp(data.get('created'))
        self.dns_name = data.get('dnsName')
        self.device_id = data.get('id')
        self.last_contact = format_timestamp(data.get('lastContact'))
        self.last_update = format_timestamp(data.get('lastUpdate'))
        self.location_id = data.get('locationId')
        self.node_class = data.get('nodeClass')
        self.node_role_id = data.get('nodeRoleId')
        self.offline = data.get('offline')
        self.organization_id = data.get('organizationId')
        self.role_policy_id = data.get('rolePolicyId')
        self.system_name = data.get('systemName')

    def __str__(self):
        # String representation for easy printing
        return (f"Device({self.device_id}, {self.system_name}, {self.dns_name}, "
                f"{self.node_class}, Offline: {self.offline})")
        
    def to_list(self):
        """ Convert the device object to a list of its attributes """
        return [
            self.device_id,
            self.system_name,
            self.dns_name,
            self.node_class,
            self.offline,
            self.organization_id,
            self.location_id,
            self.approval_status,
            self.created,
            self.last_contact,
            self.last_update
        ]        
        
def get_credentials():
    # Construct the path to the JSON file
    file_path = os.path.join('..', '_PRIVATE_', 'api_accounts.json')
    
    # Read the credentials from the JSON file
    with open(file_path, 'r') as file:
        credentials = json.load(file)                
        credentials = credentials.get(api_name, [None])[0]
        if credentials is not None:
            client_id = credentials.get('Client_ID')
            client_secret = credentials.get('Client_Secret')
            redirect_uri = credentials.get('redirect_uri')
            code = credentials.get('code')
            return client_id,client_secret, redirect_uri, code
        else:
            print("No credentials found in the file.")
            return None

def request(use_path):
    client_id,client_secret, redirect_uri, code = get_credentials()
    # Date in RFC 2616

    """
    Make a request to the NinjaOne API, with the given path.

    The request is signed with the given secret access key.

    Returns a JSON response from the API, or raises a ValueError if the
    response code is not 200.

    :param use_path: The path to query, relative to :data:`API_URL`.
    :type use_path: str
    :return: The JSON response from the API.
    :rtype: dict
    :raises ValueError: If the response code is not 200.
    """
    date_str = formatdate(timeval=None, localtime=False, usegmt=True)

    http_verb = "GET"
    content_md5 = ""  # GET Requests don't normally have a body or type
    content_type = ""
    canonicalized_resource = use_path

    string_to_sign = f"{http_verb}\n{content_md5}\n{content_type}\n{date_str}\n{canonicalized_resource}"

    # Base64 encode the UTF-8 string to sign
    utf8_encoded_string_to_sign = string_to_sign.encode("utf-8")
    base64_encoded_string_to_sign = base64.b64encode(
        utf8_encoded_string_to_sign
    ).decode("utf-8")

    # Create the HMAC-SHA1 signature using the Secret Access Key
    hmac_key = bytes(client_secret, "utf-8")
    message = base64_encoded_string_to_sign.encode("utf-8")
    signature = hmac.new(hmac_key, message, hashlib.sha1).digest()

    # Base64 encode the signature
    signature_base64 = base64.b64encode(signature).decode()

    auth_header = f"NJ {client_id}:{signature_base64}"

    headers = {"Authorization": auth_header, "Date": date_str}

    url = f"{API_URL}{use_path}"
    response = requests.get(url, headers=headers, timeout=200)

    if response.status_code == 200:
        return response.json()

    raise ValueError(f"{response.status_code} - {response.text}")


    def __str__(self):
        return f"{self.org_name} --> {self.org_locations}"

    def __iter__(self):
        yield from self.org_id

    def get_org_dict(self):
        return self.org_dict

    def get_org_name(self):
        return self.org_name

    def get_org_approval_mode(self):
        return self.org_node_approval_mode

    def get_org_id(self):
        return self.org_id

    def get_org_locations(self):
        return self.org_locations

    def get_org_policies(self):
        return self.org_policies

    def get_org_settings(self):
        return self.org_settings

def generate_signature(secret_key, method, endpoint, timestamp):
    message = f"{method}\n{endpoint}\n{timestamp}"
    signature = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()
    return base64.b64encode(signature).decode()

def get_all_organizations():
    # Replace this with the actual function that fetches user data
    results = request(ORGANIZATIONS_PATH)
    def parse_organizations(organization_data):
        """ Parse a list of dictionaries into a list of organization objects """
        return [Organization(data) for data in organization_data]

    def organizations_to_list_of_lists(organizations):
        """ Convert a list of organization objects into a list of lists """
        return [organization.to_list() for organization in organizations]

    # Headers for the organization data
    headers = ["Organization ID", "Organization Name", "Node Approval Mode"]

    # Parse the Organization data into Organization objects
    parsed_organization = parse_organizations(results)

    # Convert the parsed organization into a list of lists
    organizations_list_of_lists = organizations_to_list_of_lists(parsed_organization)

    # Include the headers with the organization data
    output_with_headers = [headers] + organizations_list_of_lists
    return output_with_headers

def get_all_locations():
    # Replace this with the actual function that fetches user data
    results = request(LOCATIONS_PATH)
    #pprint.pprint(results[:10])
    
    def parse_locations(location_data):
        """ Parse a list of dictionaries into a list of Location objects """
        return [Location(data) for data in location_data]

    def locations_to_list_of_lists(organizations):
        """ Convert a list of Location objects into a list of lists """
        return [location.to_list() for location in organizations]

    # Headers for the location data
    headers = ["Location ID", "Location Name", "Organization ID", "Addredd", "Description"]

    # Parse the location data into Location objects
    parsed_locations = parse_locations(results)

    # Convert the parsed locations into a list of lists
    locations_list_of_lists = locations_to_list_of_lists(parsed_locations)

    # Include the headers with the location data
    output_with_headers = [headers] + locations_list_of_lists
    return output_with_headers

def get_all_end_users():
    # Replace this with the actual function that fetches user data
    results = request(USERS_PATH)

    # Initialize an empty list for storing the final list of lists
    output_list = []

    # Define the headers
    headers = ["First Name", "Last Name", "Email", "User Type", "MFA", "Invitation Status", "ID", "Enabled",  "Is Admin"]

    # Add headers as the first row in output_list
    output_list.append(headers)

    # Loop through the results and extract relevant user data
    for user_dict in results:
        # Instantiate the users class with each user's data
        user_obj = User(user_dict)

        # Extract the relevant fields and add them to a list
        user_data = [
            user_obj.user_firstName,            # First Name
            user_obj.user_lastName,             # Last Name
            user_obj.user_email,                # Email
            user_obj.user_userType,             # User Type
            user_obj.user_mfaConfigured,        # MFA
            user_obj.user_invitationStatus,     # Invitation Status
            user_obj.user_administrator,        # ID (Administrator field as per your class)
            user_obj.user_enabled[0],           # Enabled (Assuming a list, extract the first value)
            #user_obj.user_deviceIds,            # Device IDs
            user_obj.user_administrator         # Is Admin (Assuming administrator is used for admin status)
        ]

        # Append the extracted data to the output_list
        output_list.append(user_data)

    #pprint.pprint(output_list[:13])
    # Return the list
    return output_list

def get_all_devices():
    # Replace this with the actual function that fetches user data
    results = request(DEVICES_PATH)
    #pprint.pprint(results[:3])

    # Define the headers
    headers = [
        "Device ID", "System Name", "DNS Name", "Node Class", "Offline", 
        "Organization ID", "Location ID", "Approval Status", "Created", 
        "Last Contact", "Last Update"
    ]
    
    def parse_devices(device_data):
        """ Parse a list of dictionaries into a list of Device objects """
        return [Device(data) for data in device_data]

    def devices_to_list_of_lists(devices):
        """ Convert a list of Device objects into a list of lists """
        return [device.to_list() for device in devices]

    parsed_results = devices_to_list_of_lists(parse_devices(results))
    output_with_headers = [headers] + parsed_results
    return output_with_headers

def get_all_roles():
    # Replace this with the actual function that fetches user data
    results = request(ROLES_PATH)
    return
    # Define the headers
    headers = [
        "Device ID", "System Name", "DNS Name", "Node Class", "Offline", 
        "Organization ID", "Location ID", "Approval Status", "Created", 
        "Last Contact", "Last Update"
    ]
    
    def parse_devices(device_data):
        """ Parse a list of dictionaries into a list of Device objects """
        return [Device(data) for data in device_data]

    def devices_to_list_of_lists(devices):
        """ Convert a list of Device objects into a list of lists """
        return [device.to_list() for device in devices]

    parsed_results = devices_to_list_of_lists(parse_devices(results))
    output_with_headers = [headers] + parsed_results
    return output_with_headers
    
if __name__ == "__main__":
    results = get_all_end_users()
    pprint.pprint(results[:10])


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
api_name = 'sentinelone'
API_URL = "https://app.ninjarmm.com"
PATH = "/v2/users"


# Your SentinelOne API URL and API key
S1_API_URL = "https://usea1-ninjaone2.sentinelone.net/web/api/v2.1"

def get_credentials():
    # Construct the path to the JSON file
    file_path = os.path.join('..', '_PRIVATE_', 'api_accounts.json')
    
    # Read the credentials from the JSON file
    with open(file_path, 'r') as file:
        credentials = json.load(file)                
        credentials = credentials.get(api_name, [None])[0]
        if credentials is not None:
            api_key = credentials.get('api_key')
            return api_key
        else:
            print("No credentials found in the file.")
            return None


# Function to establish a connection
def get_users():
    api_key = get_credentials()
    
    headers = {
        'Authorization': f'ApiToken {api_key}',
        'Content-Type': 'application/json'
    }

    # Example endpoint to test connection (retrieving account information)
    endpoint = f"{S1_API_URL}/users"

    try:
        # Send GET request
        response = requests.get(endpoint, headers=headers)

        # Check if the response was successful
        if response.status_code == 200:
            print("Connection successful!")
            return response.json()  # Return the response data as JSON
        else:
            print(f"Failed to connect. Status code: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"Error connecting to SentinelOne: {str(e)}")
        
def get_devices():
    api_key = get_credentials()  # Ensure this function retrieves your API key correctly
    
    headers = {
        'Authorization': f'ApiToken {api_key}',
        'Content-Type': 'application/json'
    }

    # Endpoint to retrieve agents (devices)
    endpoint = f"{S1_API_URL}/agents"

    def convert_to_flat_list_of_lists(devices_list, keys):
        list_of_lists = [keys]  # Include headers as the first row
        for device in devices_list:
            if isinstance(device, dict):  # Ensure device is a dictionary
                row = []
                for key in keys:
                    value = device.get(key, 'N/A')  # Default to 'N/A' if missing
                    # Handle lists and complex types
                    if isinstance(value, list):
                        # Flatten the list to a string or handle as needed
                        row.append(', '.join(map(str, value)) if value else '')  # Join list values into a string
                    elif isinstance(value, dict):
                        # If you encounter a dict, flatten it or convert to string
                        row.append(str(value))  # Convert dict to string
                    elif value is None:
                        row.append('')  # Replace null with an empty string
                    else:
                        row.append(value)  # Append the value as is
                list_of_lists.append(row)
        return list_of_lists

    try:
        # Send GET request
        response = requests.get(endpoint, headers=headers)

        # Check if the response was successful
        if response.status_code == 200:
            print("Successfully retrieved all devices.")
            results = response.json().get('data', [])  # Extract the 'data' field
            if results:  # Ensure there are results to process
                dictionary_keys = get_all_keys_from_list_of_dicts(results)
                #list_of_lists = convert_to_list_of_lists(results, dictionary_keys)
                flattened_list_of_devices = convert_to_flat_list_of_lists(results, dictionary_keys)
                return flattened_list_of_devices  # Return the list of lists
            else:
                print("No devices found.")
                return []
        else:
            print(f"Failed to retrieve devices. Status code: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"Error connecting to SentinelOne: {str(e)}")        
    
if __name__ == "__main__":
    # Call the function to connect
    #results = get_users()
    results = get_devices()
    pprint.pprint(results)


import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '_GITHUB_')))
from _SHARED_._common_imports import *

import requests, json, pprint

with open(
    '_SHARED_\\api_accounts.json',
    'r') as api_accounts:
    api_keys = json.load(api_accounts)
api_info = api_keys['mysonicwall'][0]['api_key']

def get_cloud_tenants():
    # Define the API endpoint and your API key
    api_url = "https://api.mysonicwall.com/api/hgms/get-cloud-tenants"
    api_key = api_info

    # Set the headers for authentication
    headers = {
        'X-Api-Key': api_key
    }

    # Define query parameters
    params = {
        'isforced': 'false',
        'bisfromCSC2': 'false',
        'limit': 1
    }

    # Make a request to the API
    response = requests.get(api_url, headers=headers, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Parse the JSON response
        devices = response.json()
        print(f'Count of Cloud Tenants:', len(devices))
        pprint.pprint(devices)

    else:
        print(f"Failed to retrieve devices: {response.status_code}")
    
def get_device_info():
    # Define the API endpoint and your API key
    deviceSerial = "0017C577D2D9"  # Replace with your device
    api_url = "https://api.mysonicwall.com/api/downloads/"+deviceSerial
    print("api_url:", api_url)
    api_key = api_info

    # Set the headers for authentication
    headers = {
        'X-Api-Key': api_key
    }

    # Define query parameters
    params = {
        'username': '433747'
    }
    # Make a request to the API
    response = requests.get(api_url, headers=headers, params=params)
    print(response)
    # Check the response status code
    if response.status_code == 200:
        # Parse the JSON response
        devices = response.json()
        pprint.pprint(devices)
    else:
        print(f"Failed to retrieve device: {response.status_code}")
    """
    """
    
def main():
    try:
        service = get_cloud_tenants()
        #service = get_device_info()
        print('Success.\n')
    except Exception as err:
        print(f"An error occurred: {err}")

if __name__ == '__main__':
    main()

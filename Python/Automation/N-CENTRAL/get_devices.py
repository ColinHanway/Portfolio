import requests
jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJTb2xhcndpbmRzIE1TUCBOLWNlbnRyYWwiLCJ1c2VyaWQiOjEwOTIyMDMxMjUsImlhdCI6MTcyMjI5MTUxMH0.4bfqV--mOvTiVHHPjpQV877X2EYnTryDs06A-WQn1r0"
server_url = "https://ncentral.alphamediausa.com"

import requests

# Replace these with your actual server URL and JWT
auth_endpoint = "/api/auth/authenticate"
api_endpoint = "/dms/services/DeviceService"
ca_cert_path = "./_.alphamediausa.com.crt"

# Construct the full authentication URL
auth_url = f"{server_url}{auth_endpoint}"

print(f'\nAuth URL: {auth_url}\n')

# Set up the authentication headers
auth_headers = {
    'Authorization': f'Bearer {jwt_token}',
    'Content-Type': 'application/json'
}

# Authenticate and get access and refresh tokens
try:
    auth_response = requests.post(auth_url, headers=auth_headers, verify=False)
    auth_response.raise_for_status()  # Raise an HTTPError for bad responses

    auth_data = auth_response.json()
    access_token = auth_data['access_token']
    refresh_token = auth_data['refresh_token']

    # Construct the full API URL
    api_url = f"{server_url}{api_endpoint}"

    # Set up the API request headers with the access token
    api_headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Define the payload to request device information
    payload = {
        "method": "getDevices",
        "params": {},
        "id": 1
    }

    # Make the API request
    response = requests.post(api_url, json=payload, headers=api_headers, verify=False)
    response.raise_for_status()  # Raise an HTTPError for bad responses

    # Parse the response JSON
    data = response.json()

    # Extract device hostnames
    if 'result' in data and 'devices' in data['result']:
        devices = data['result']['devices']
        hostnames = [device['hostname'] for device in devices]

        # Print the list of hostnames
        print("Device Hostnames:")
        for hostname in hostnames:
            print(hostname)
    else:
        print("No devices found or unexpected response format.")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###

# API endpoints
api_url = "https://api.nuclias.com"

def set_credentials():
    # Authentication (replace with your credentials and scopes)
    with open(
        '_PRIVATE_\\api_accounts.json', 'r'
        ) as credentials_file:
        credentials = json.load(credentials_file)
        credentials = credentials.get('nuclias', [None])[0]
        if credentials is not None:
                return credentials.get('api_key')
        else:
            print("No 'nuclias' credentials found in the file.")
            return None
        
def get_devices():           
    # Credentials
    credentials = set_credentials()
    #print(f'api_key = {credentials}')

    headers = {
        'Authorization': f'Bearer {credentials}',  # Adjust according to the required auth method
        'Content-Type': 'application/json'
    }

    params = {
        'limit': 1
    }

    try:
        endpoint = '/api/v1/auth/gui/bootstrap'
        api_endpoint= api_url+endpoint
        # Make a GET request to the API endpoint
        response = requests.get(api_endpoint, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
    except requests.exceptions.RequestException as e:
        print(f"Error accessing the API: {e}")

    # Parse the JSON response
    try:
        data = response.json()
        #pprint.pprint(data)
        all_devices = []
        sheets_data = []

        headers = [
            'Name', 'UID', 'Device model Name', 'Firmware Version', 
            'IP Address', 'Name Server 1', 'Name Server 2', 
            'Online Clients', 'Last Updated', 'Last Offline', 
            'Last Online', 'License Key', 'License Period', 
            'License Bound', 'Time Remaining'
        ]
        sheets_data = [headers]

        
    # Check if 'orgChildren' key exists and is an object
        if 'orgChildren' in data and isinstance(data['orgChildren'], dict):
            org_children = [data['orgChildren']]  # Wrap single object in a list for iteration
        else:
            print("Error: 'orgChildren' key is missing or not an object.")
            return all_devices
        #print("Organization Children: %s" % len(org_children))
        #print(org_children[:1]) # Print
        
        field_counts1 = {field: 0 for field in org_children[0].keys()}
        field_counts2 = {field: 0 for field in device_groups[0].keys()}

        for record in org_children:
            for field in field_counts1.keys():
                if field in record:
                    field_counts1[field] += 1

        # Print counts for each field
        for field, count in field_counts1.items():
            print(f"{field}: {count}")
            
        for record in org_children:
            tenant = record.get('tenant', 'Not Available')  # 'Not Available' is a default value if 'tenant' is not found
            print(f"Tenant: {tenant}")
            
        for org in org_children:
            device_groups = org.get('deviceGroups', [])
            #print("Device Groups: %s" % len(device_groups))
            #print(device_groups[:1]) # Print
        
        for record in device_groups:
            for field in field_counts2.keys():
                if field in record:
                    field_counts2[field] += 1

        # Print counts for each field
        for field, count in field_counts2.items():
            print(f"{field}: {count}")
          
            for tenants in device_groups:
                tenants = tenants.get('tenant', [])
                #print("Tenants: %s)" % len(tenants))
            for device_group in device_groups:
                devices = device_group.get('devices', [])
                for device in devices:
                    all_devices.append(device)
                    for device in all_devices:
                        for license in device.get('licenses', []):
                            entry = [
                                device.get('name', ''),
                                device.get('uid', ''),
                                device.get('deviceModel', {}).get('name', ''),
                                device.get('firmwareRevision', ''),
                                device.get('ipAddress', ''),
                                device.get('nameserver1', ''),
                                device.get('nameserver2', ''),
                                device.get('numOnlineClients', 0),
                                format_timestamp(device.get('lastUpdatedAt')),
                                format_timestamp(device.get('lastOfflineTime'), with_time=True),
                                format_timestamp(device.get('lastOnlineTime'), with_time=True),
                                license.get('key', ''),
                                license.get('period', ''),
                                license.get('boundAt', '')[:10],  # Extract just the date part
                                license.get('timeRemaining', '')
                            ]
                            sheets_data.append(entry)
            print("All devices: %s" % len(all_devices))
        
        # Export to CSV file
        with open('dlink_org_children.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(org_children)
        # Export to CSV file
        with open('dlink_device_groups.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(device_groups)
       
        
        return sheets_data

    except requests.exceptions.RequestException as e:
        print(f"Error accessing devices: {e}")
   
    # Print the device information

# Main execution
def main():
    try:
        results = get_devices()
        #pprint.pprint(results[:3])

    except Exception as e:
        print(f"An error occurred: {e}")
        
        
if __name__ == '__main__':
    main()
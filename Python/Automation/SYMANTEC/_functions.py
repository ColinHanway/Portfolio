### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###
from concurrent.futures import ThreadPoolExecutor, as_completed

api_name = "symantec"

def get_credentials():  # Added api_name as parameter for flexibility
    # Load API credentials from the file
    file_path = os.path.join('_PRIVATE_', 'api_accounts.json')
    with open(file_path, 'r') as api_accounts:
        api_keys = json.load(api_accounts)
    
    # Extract credentials based on the provided API name
    client_id = api_keys[api_name][0]["client_id"]
    client_secret = api_keys[api_name][0]["client_secret"]
    token_url = api_keys[api_name][0]["token_url"]
    
    return client_id, client_secret, token_url

def get_access_token():
    client_id, client_secret, token_url = get_credentials()

    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(f'Failed to obtain access token: {response.status_code} - {response.text}')
        return None
        
def fetch_device_id_list_old():
    access_token = get_access_token()
    devices_url = 'https://api.sep.securitycloud.symantec.com/v1/devices'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'limit': 100,  # Limiting to 1800 results
        'offset': 0  # Start from the first batch
    }
    
        
    deviceList = []

    response = requests.get(devices_url, headers=headers, params=params)
    devices = response.json()
    total_devices = devices['total']
    #total_devices = 20

    print(f'Fetching {total_devices} devices...')

    with tqdm(total=total_devices, desc="Progress") as pbar:
        while True:
            response = requests.get(devices_url, headers=headers, params=params)
            devices = response.json()
            
            
            # Break the loop if no more devices are fetched
            if len(deviceList) >= total_devices:
                break
            
            for device in devices.get('devices', []):
                try:
                    deviceID = device['id']
                except KeyError:
                    deviceID = ''

                each_record = [
                    deviceID
                ]
                deviceList.append(each_record)

            # Update offset to get the next batch
            params['offset'] += params['limit']
            
            # Update the progress bar with the number of devices fetched in this batch
            pbar.update(len(devices.get('devices', [])))
            
    return deviceList

def fetch_devices_list():
    access_token = get_access_token()
    devices_url = 'https://api.sep.securitycloud.symantec.com/v1/devices'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'limit': 1000,  # Limiting to 1800 results
        'offset': 0  # Start from the first batch
    }
    
        
    deviceList = []
    columnHeaders = [
                'Hostname',
                'Domain',
                'Group Name',
                'Parent Group ID',
                'OS Name',
                'Last User',
                'Serial',
                'Last Modified',
                'Connection Status',
                'Device Status'
            ]
    deviceList.append(columnHeaders)

    # Initial request to get the total number of devices
    response = requests.get(devices_url, headers=headers, params=params)
    response.raise_for_status()  # Catch HTTP errors

    devices = response.json()
    total_devices = devices.get('total', 0)
    
    # Use tqdm to show progress for fetching and processing each device
    with tqdm(total=total_devices, desc="Processing Devices", unit="device") as pbar:
        while True:
            response = requests.get(devices_url, headers=headers, params=params)
            response.raise_for_status()

            devices = response.json()

            # Iterate over each device in the current batch
            for device in devices['devices']:
                deviceOSName = device.get('os', {}).get('name', '')
                deviceHost = device.get('host', '')
                deviceDomain = device.get('domain', '')
                lastUser = device.get('os', {}).get('user', '')
                deviceSerial = device.get('hw', {}).get('serial', 'unknown')
                deviceGroupName = device.get('parent_device_group_name', 'unknown')
                deviceGroupID = device.get('parent_device_group_id', 'unknown')
                connectionStatus = device.get('connection_status', 'unknown')
                
                # Convert last modified date to 'YYYY-MM-DD' format
                lastModified = device.get('modified')
                if lastModified:
                    try:
                        lastModified = datetime.fromisoformat(lastModified[:-1]).date().strftime("%Y-%m-%d")
                    except ValueError:
                        lastModified = 'unknown'
                else:
                    lastModified = 'unknown'
                
                DeviceStatus = device.get('device_status', 'unknown')

                each_record = [
                    deviceHost,
                    deviceDomain,
                    deviceGroupName,
                    deviceGroupID,
                    deviceOSName,
                    lastUser,
                    deviceSerial,
                    lastModified,
                    connectionStatus,
                    DeviceStatus
                ]
                deviceList.append(each_record)
                
                # Update the progress bar for each device processed
                pbar.update(1)
            
            if len(deviceList) - 1 >= total_devices:
                break
            
            params['offset'] += params['limit']  # Move offset to next batch

    return deviceList

def format_date(date_str):
    """Convert a timestamp string to 'YYYY/MM/DD' format."""
    try:
        # Assuming the date string is in ISO 8601 format
        date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))  # Adjust for UTC time
        return date_obj.strftime('%Y/%m/%d')
    except (TypeError, ValueError):
        return 'unknown'
    
def fetch_groups_list():
    access_token = get_access_token()
    groups_url = 'https://api.sep.securitycloud.symantec.com/v1/device-groups'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'limit': 300,  # Limiting to 300 results
        'offset': 0  # Start from the first batch
    }
    
        
    groupList = []
    columnHeaders = [
                'Name',
                'ID',
                'Description',
                'Parent ID',
                'Created',
                'Modified'
            ]
    groupList.append(columnHeaders)
    
    while True:
        response = requests.get(groups_url, headers=headers, params=params)
        response.raise_for_status()  # Ensure we catch HTTP errors

        groups = response.json()

        if len(groupList) < groups['total']:
            params['offset'] += params['limit']  # Move offset to next batch
        else:
            break  # Exit loop if all devices have been fetched

        # Wrap the iteration with tqdm for a progress bar
        for group in tqdm(groups['device_groups'], desc="Parsing Groups", unit="group"):
            groupName = group.get('name', '')
            groupID = group.get('id', '')
            description = group.get('description', '')
            parentID = group.get('parent_id', '')
            # Parse and format the 'created' and 'modified' fields
            created_raw = group.get('created')
            modified_raw = group.get('modified')

            # Convert timestamps to 'YYYY/MM/DD' format if present
            created = format_date(created_raw)
            modified = format_date(modified_raw)
            each_record = [
                groupName,
                groupID,
                description,
                parentID,
                created,
                modified
            ]
            groupList.append(each_record)

    return groupList

def fetch_device_details(device_id):
    access_token = get_access_token()
    
    url = 'https://api.sep.securitycloud.symantec.com/v1/devices/'+device_id

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    details = response.json()
    #pprint.pprint(details)
        
    return details

def fetch_device_details_batch_old(device_ids):
    access_token = get_access_token()
    
    url = 'https://api.sep.securitycloud.symantec.com/v1/devices'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    payload = {'device_ids': device_ids}
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        print("Response content:", response.text)
        response.raise_for_status()  # This will raise an HTTPError for bad responses
    
    try:
        details = response.json()
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print("Response content:", response.text)
        raise
    
    return details

def fetch_devices_details_from_list_batch_old():
    device_ids = fetch_device_id_list_old()
    
    try:
        flattened_device_ids = [device_id[0] if isinstance(device_id, list) else device_id for device_id in device_ids]
    except TypeError as e:
        print(f"Error processing device IDs: {e}")
        return

    # Batch size for API calls
    batch_size = 100
    device_details_list = []

    with tqdm(total=len(flattened_device_ids), desc="Processing Device Details") as pbar:
        for i in range(0, len(flattened_device_ids), batch_size):
            batch_ids = flattened_device_ids[i:i+batch_size]
            
            # Fetch device details in batch
            device_info_list = fetch_device_details_batch_old(batch_ids)
            
            # Process each device info
            for device_info in device_info_list.get('devices', []):
                device_info_row = [
                    device_info.get('host', ''),
                    device_info.get('name', ''),
                    device_info.get('hw', {}).get('model_vendor', ''),
                    device_info.get('hw', {}).get('serial', ''),
                    device_info.get('connection_status', ''),
                    device_info.get('created', ''),
                    device_info.get('domain', ''),
                    device_info.get('id', ''),
                    device_info.get('is_virtual', ''),
                    device_info.get('os', {}).get('name', ''),
                    device_info.get('os', {}).get('type', ''),
                    device_info.get('os', {}).get('ver', ''),
                    device_info.get('os', {}).get('user_domain', ''),
                    device_info.get('os', {}).get('user', ''),
                    device_info.get('parent_device_group_id', ''),
                    device_info.get('parent_device_group_name', ''),
                ]

                # Extracting features information
                for product in device_info.get('products', []):
                    for feature in product.get('features', []):
                        feature_info = [
                            feature.get('name', ''),
                            feature.get('security_status', ''),
                            feature.get('status', ''),
                            feature.get('engine_version', ''),
                            feature.get('content_last_download_time', ''),
                            feature.get('content_version', ''),
                        ]
                        # Combine device info with feature info for each feature
                        device_details_list.append(device_info_row + feature_info)
                
            # Update the progress bar
            pbar.update(len(batch_ids))

    return device_details_list

def fetch_devices_details_from_list():

    device_ids = fetch_device_id_list()
    #device_ids = device_ids[:2]
    
    # Assuming device_ids is a list of lists, but need to handle if it's a list of strings
    try:
        flattened_device_ids = [device_id[0] if isinstance(device_id, list) else device_id for device_id in device_ids]
    except TypeError as e:
        print(f"Error processing device IDs: {e}")
        return    
    
    #pprint.pprint(flattened_device_ids)
    #print(f'Processing {total_devices} devices')

    # Define the column headers
    column_headers = [
        'hostname', 'name', 'vendor', 'serial', 'Connection Status',
        'Date Created', 'Domain', 'ID', 'Is Virtual', 'OS Name', 'OS Type',
        'OS Version', 'Domain', 'Last Logged On User', 'Parent Group',
        'Group Name', 'Feature Name', 'Security Status', 'Status', 'Version',
        'Last Downloaded', 'Content Version'
    ]
    device_details_list = [column_headers]

# Iterate over each device ID and make a request to the API
    with tqdm(total=len(flattened_device_ids), desc="Processing Device Details") as pbar:
        for device in flattened_device_ids:
            #print(f'\nProcessing Device: {device}\n')
            
            # Fetch device details
            device_info = fetch_device_details(device)

            # Extracting the general device information
            device_info_row = [
                device_info.get('host', ''),
                device_info.get('name', ''),
                device_info.get('hw', {}).get('model_vendor', ''),
                device_info.get('hw', {}).get('serial', ''),
                device_info.get('connection_status', ''),
                device_info.get('created', ''),
                device_info.get('domain', ''),
                device_info.get('id', ''),
                device_info.get('is_virtual', ''),
                device_info.get('os', {}).get('name', ''),
                device_info.get('os', {}).get('type', ''),
                device_info.get('os', {}).get('ver', ''),
                device_info.get('os', {}).get('user_domain', ''),
                device_info.get('os', {}).get('user', ''),
                device_info.get('parent_device_group_id', ''),
                device_info.get('parent_device_group_name', ''),
            ]

            # Extracting features information
            for product in device_info.get('products', []):
                for feature in product.get('features', []):
                    feature_info = [
                        feature.get('name', ''),
                        feature.get('security_status', ''),
                        feature.get('status', ''),
                        feature.get('engine_version', ''),
                        feature.get('content_last_download_time', ''),
                        feature.get('content_version', ''),
                    ]
                    # Combine device info with feature info for each feature
                    device_details_list.append(device_info_row + feature_info)

                # Update the progress bar for each device processed
                pbar.update(1)
    pprint.pprint(device_details_list[:3])
    return device_details_list

def fetch_device_id_list():
    access_token = get_access_token()
    devices_url = 'https://api.sep.securitycloud.symantec.com/v1/devices'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'limit': 100,  # Limiting to 100 results per request
        'offset': 0  # Start from the first batch
    }
    
    deviceList = []

    response = requests.get(devices_url, headers=headers, params=params)
    devices = response.json()
    total_devices = devices['total']

    print(f'Fetching {total_devices} devices...')

    with tqdm(total=total_devices, desc="Progress") as pbar:
        while True:
            response = requests.get(devices_url, headers=headers, params=params)
            devices = response.json()
            
            if len(deviceList) >= total_devices:
                break
            
            for device in devices.get('devices', []):
                try:
                    deviceID = device['id']
                except KeyError:
                    deviceID = ''

                each_record = [deviceID]
                deviceList.append(each_record)

            params['offset'] += params['limit']
            pbar.update(len(devices.get('devices', [])))
            
    return deviceList

def fetch_device_details(device_id):
    access_token = get_access_token()
    
    url = f'https://api.sep.securitycloud.symantec.com/v1/devices/{device_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Device ID {device_id} - Received status code {response.status_code}")
        return None
    
    try:
        details = response.json()
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON decode error for Device ID {device_id}: {e}")
        return None
    
    return details

def fetch_devices_details_from_list_concurrent():
    device_ids = fetch_device_id_list()
    
    try:
        flattened_device_ids = [device_id[0] if isinstance(device_id, list) else device_id for device_id in device_ids]
    except TypeError as e:
        print(f"Error processing device IDs: {e}")
        return
    
    # Define the column headers
    column_headers = [
        'hostname', 'name', 'vendor', 'serial', 'Connection Status',
        'Date Created', 'Domain', 'ID', 'Is Virtual', 'OS Name', 'OS Type',
        'OS Version', 'Domain', 'Last Logged On User', 'Parent Group',
        'Group Name', 'Feature Name', 'Security Status', 'Status', 'Version',
        'Last Downloaded', 'Content Version'
    ]
    device_details_list = [column_headers]

    # Use ThreadPoolExecutor for concurrent requests
    with ThreadPoolExecutor(max_workers=100) as executor:  # Adjust max_workers based on your needs
        futures = {executor.submit(fetch_device_details, device_id): device_id for device_id in flattened_device_ids}
        
        with tqdm(total=len(flattened_device_ids), desc="Processing Device Details") as pbar:
            for future in as_completed(futures):
                device_id = futures[future]
                try:
                    device_info = future.result()
                    if device_info:
                        device_info_row = [
                            device_info.get('host', ''),
                            device_info.get('name', ''),
                            device_info.get('hw', {}).get('model_vendor', ''),
                            device_info.get('hw', {}).get('serial', ''),
                            device_info.get('connection_status', ''),
                            device_info.get('created', ''),
                            device_info.get('domain', ''),
                            device_info.get('id', ''),
                            device_info.get('is_virtual', ''),
                            device_info.get('os', {}).get('name', ''),
                            device_info.get('os', {}).get('type', ''),
                            device_info.get('os', {}).get('ver', ''),
                            device_info.get('os', {}).get('user_domain', ''),
                            device_info.get('os', {}).get('user', ''),
                            device_info.get('parent_device_group_id', ''),
                            device_info.get('parent_device_group_name', ''),
                        ]

                        for product in device_info.get('products', []):
                            for feature in product.get('features', []):
                                feature_info = [
                                    feature.get('name', ''),
                                    feature.get('security_status', ''),
                                    feature.get('status', ''),
                                    feature.get('engine_version', ''),
                                    feature.get('content_last_download_time', ''),
                                    feature.get('content_version', ''),
                                ]
                                device_details_list.append(device_info_row + feature_info)
                except Exception as e:
                    print(f"Error fetching details for Device ID {device_id}: {e}")

                pbar.update(1)

    return device_details_list

# Main execution
def main():
    device_id = 'zupvGpMnRMKoiQq5SgeuIg'
    
    #result = fetch_device_id_list()
    #result = fetch_devices_list()
    #result = fetch_groups_list()
    #result = fetch_device_details(device_id)
    #result = fetch_devices_details_from_list_batch_old()
    result = fetch_devices_details_from_list_concurrent()
    #print("Success\n")
    #pprint.pprint(result)


if __name__ == '__main__':
    main()
### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_error_messages(file_path):
    with open(file_path) as error_map_file:
        error_map = json.load(error_map_file)
        return error_map['error_code_map']

def display_error_message(code, error_code_map):
    error = next((e for e in error_code_map if e['code'] == code), None)
    if error:
        print(f"Error message: {error['message']}")
    else:
        print("Unknown error code")
        
def get_zone_id(zone_name):
    credentials = get_credentials('cloudflare')

    url = f'https://api.cloudflare.com/client/v4/zones'
    headers = {
        'Authorization': credentials,  # Use the token directly as 'Bearer <API_TOKEN>'
        'Content-Type': 'application/json'
    }
    print(headers)
    params = {
        'name': zone_name
    }
    response = requests.get(url, headers=headers, params=params)
    response_data = response.json()

    if response_data['success']:
        for zone in response_data['result']:
            if zone['name'] == zone_name:
                return zone['id']
    else:
        raise Exception(f"Failed to get zone ID: {response_data['errors']}")

def get_dns_records(zone_id):
    credentials = get_credentials('cloudflare')

    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
    headers = {
        'Authorization': credentials,  # Use the token directly as 'Bearer <API_TOKEN>'
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()

    if response_data['success']:
        return response_data['result']
    else:
        raise Exception(f"Failed to get DNS records: {response_data['errors']}")
    
def get_domains_from_sheet(spreadsheet_id=3, range_name=97):
    """
    Read a list of domains from a specified Google Sheets range.
    
    :param spreadsheet_id: The ID of the Google Spreadsheet.
    :param range_name: The range of cells to read from (e.g., 'Sheet1!A:A').
    :return: List of domains read from the sheet.
    """
    try:
        # Get the values from the sheet
        results = gs.read_sheet(spreadsheet_id, range_name)
        #print(results)

        # Check if there is any data
        if not results:
            print("No data found.")
            return []

        # Extract domains from the values list
        domains = [col[1] for col in results if col]  # Assuming domains are in the first [0] column
        #print(domains)
        return domains[1:] # Skip the header row
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_all_zones():
    """
    Retrieve all zones from the Cloudflare account.
    
    :param api_token: Cloudflare API token.
    :return: List of zone dictionaries with detailed information.
    """
    def safe_join(iterable):
        """
        Safely join elements of an iterable into a string, or return an empty string if the iterable is None.
        
        :param iterable: The iterable to join.
        :return: A string with joined elements or an empty string.
        """
        if isinstance(iterable, list):
            return ', '.join(iterable)
        return ''

    credentials = get_credentials('cloudflare')
    
    url = 'https://api.cloudflare.com/client/v4/zones'
    headers = {
        'Authorization': credentials,
        'Content-Type': 'application/json'
    }
    zones = []
    page = 1

    while True:
        params = {
            'page': page,
            'per_page': 50  # You can increase this to 50 if needed
        }
        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()

        if response_data.get('success'):
            zones.extend(response_data.get('result', []))
            result_info = response_data.get('result_info', {})

            # Print debug information
            print(f"Page {page}: Retrieved {len(response_data.get('result', []))} zones.")
            print(f"Result info: {result_info}")

            # Check if there are more pages to retrieve
            if page >= result_info.get('total_pages', 0):
                break

            page += 1
        else:
            raise Exception(f"Failed to get zones: {response_data.get('errors')}")
                
    # Format the zones data into rows
    headers = [
        'Zone Name', 
        'Zone ID', 
        'Account ID', 
        'Account Name', 
        'Activated On', 
        'Created On',
        'Development Mode', 
        'Custom Certificate Quota',
        'Page Rule Quota', 
        'Phishing Detected', 
        'Step',
        'Modified On', 
        'Name Servers',
        'Original DNS Host', 
        'Original Name Servers',
        'Original Registrar', 
        'Owner Email', 
        'Owner ID',
        'Owner Type', 
        'Paused', 
        'Permissions',
        'Plan ID', 
        'Plan Name', 
        'Plan Price', 
        'Plan Currency',
        'Plan Subscribed', 
        'Status', 
        'Tenant ID', 
        'Tenant Name',
        'Tenant Unit ID', 
        'Zone Type'
    ]

    #results = [headers]
    results = []
    
    for zone in zones:
        row = [
            zone.get('name'),
            zone.get('id'),
            zone.get('account', {}).get('id'),
            zone.get('account', {}).get('name'),
            format_date(zone.get('activated_on')),
            format_date(zone.get('created_on')),
            zone.get('development_mode'),
            zone.get('meta', {}).get('custom_certificate_quota'),
            zone.get('meta', {}).get('page_rule_quota'),
            zone.get('meta', {}).get('phishing_detected'),
            zone.get('meta', {}).get('step'),
            format_date(zone.get('modified_on')),
            safe_join(zone.get('name_servers')),
            zone.get('original_dnshost'),
            safe_join(zone.get('original_name_servers')),
            zone.get('original_registrar'),
            zone.get('owner', {}).get('email'),
            zone.get('owner', {}).get('id'),
            zone.get('owner', {}).get('type'),
            zone.get('paused'),
            safe_join(zone.get('permissions')),
            zone.get('plan', {}).get('id'),
            zone.get('plan', {}).get('name'),
            zone.get('plan', {}).get('price'),
            zone.get('plan', {}).get('currency'),
            zone.get('plan', {}).get('is_subscribed'),
            zone.get('status'),
            zone.get('tenant', {}).get('id'),
            zone.get('tenant', {}).get('name'),
            zone.get('tenant_unit', {}).get('id'),
            zone.get('type')
        ]
        results.append(row)

    return results

def transform_dns_records_for_sheets(records):
   
    # Create a list to hold the data rows
    data_rows = []
    
    # Transform each DNS record into a row
    for record in records:
        row = [
            record.get('zone_name'),
            record.get('zone_id'),
            record.get('name'),
            record.get('id'),
            record.get('type'),
            record.get('content'),
            record.get('ttl'),
            record.get('proxiable'),
            record.get('proxied'),
            format_date(record.get('created_on')),  # Convert to yyyy-mm-dd
            format_date(record.get('modified_on')), # Convert to yyyy-mm-dd
            record.get('comment')
        ]
        data_rows.append(row)
    
    return data_rows

def main():
    try:
        print('Testing function...\n')
        #results = get_credentials('cloudflare')
        #results = get_zone_id('1009theeagle.com')
        #results = get_dns_records(results)
        #results = transform_dns_records_for_sheets(results)
        results = get_domains_from_sheet()
        #print(results)
        print('Test: Success\n')
        pprint.pprint(results)
    except Exception as err:
        print(f"Test: Failure\n{err}")

if __name__ == '__main__':
    main()

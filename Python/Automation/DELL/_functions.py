### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###

service = "dell techdirect warranty"
def get_credentials_dell_warranty_api():
    with open(
        '_PRIVATE_\\api_accounts.json', 'r'
        ) as credentials_file:
        credentials = json.load(credentials_file)
        credentials = credentials.get('dell techdirect warranty', [None])[0]
        if credentials is not None:
            client_id = credentials.get('Client_ID')
            client_secret = credentials.get('Client_Secret')
            token_url = credentials.get('token_url')
            return client_id,client_secret, token_url
        else:
            print("No 'nuclias' credentials found in the file.")
            return None

def get_credentials_dell_support_api():
    with open(
        '_PRIVATE_\\api_accounts.json', 'r'
        ) as credentials_file:
        credentials = json.load(credentials_file)
        credentials = credentials.get('dell techdirect support', [None])[0]
        if credentials is not None:
            client_id = credentials.get('Client_ID')
            client_secret = credentials.get('Client_Secret')
            token_url = credentials.get('token_url')
            return client_id,client_secret, token_url
        else:
            print("No 'nuclias' credentials found in the file.")
            return None

def get_access_token(service_name):
    if service_name == "warranty":
        client_id,client_secret, token_url = get_credentials_dell_warranty_api()      
    if service_name == "support":
        client_id,client_secret, token_url = get_credentials_dell_support_api()      
    
    
    # Request payload
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    }

    # Request headers
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Send the request
    response = requests.post(token_url, data=payload, headers=headers)
    #print(response)
    # Check if the request was successful
    if response.status_code == 200:
        # Extract the JWT from the response
        token_data = response.json()
        access_token = token_data.get('access_token')
        #print(f"Access Token (JWT): {access_token}")
        return access_token
    else:
        print(f"Failed to obtain token. Status code: {response.status_code}")
        print(f"Response: {response.text}")
            
def get_device_info_by_service_tag(service_tag):           
    # Credentials
    service = "warranty"
    jwt = get_access_token(service)
    #print(f"Access Token: {jwt}")
    asset_details_url = "https://apigtwb2c.us.dell.com/PROD/sbil/eapi/v5/asset-components"
   
    
    headers = {
        'Authorization': f'Bearer {jwt}',
        'Content-Type': 'application/json'
    }
    params = {
        'servicetag': service_tag
    }
    #print(headers, params)
    
    response = requests.get(asset_details_url, headers=headers, params=params)
    if response.status_code == 200:
        #pprint.pprint(response)
        return response.json()
    else:
        raise Exception(f"Failed to retrieve warranty status: {response.status_code} - {response.text}")

def get_asset_header_by_service_tag(service_tag):           
    # Credentials
    service = "warranty"
    jwt = get_access_token(service)

    asset_details_url = "https://apigtwb2c.us.dell.com/PROD/sbil/eapi/v5/assets"
    
    headers = {
        'Authorization': f'Bearer {jwt}',
        'Content-Type': 'application/json'
    }
    params = {
        'servicetags': service_tag
    }
    
    response = requests.get(asset_details_url, headers=headers, params=params)
    if response.status_code == 200:
        asset_header_info = response.json()
        cleaned_data = clean_asset_header_info(asset_header_info)
        return cleaned_data
    else:
        raise Exception(f"Failed to retrieve asset header info: {response.status_code} - {response.text}")

def get_warranty_info_by_service_tag(service_tag):
    # Credentials
    service = "warranty"
    jwt = get_access_token(service)

    warranty_url = f'https://apigtwb2c.us.dell.com/PROD/sbil/eapi/v5/asset-entitlements'
    headers = {
        'Authorization': f'Bearer {jwt}',
        'Content-Type': 'application/json'
    }
    params = {
        'servicetags': service_tag
        }
    
    response = requests.get(warranty_url, headers=headers, params=params)
    
    if response.status_code == 200:
        warranty_info = response.json()
        cleaned_data = clean_warranty_info(warranty_info)
        return cleaned_data
    else:
        raise Exception(f"Failed to retrieve warranty status: {response.status_code} - {response.text}")

def clean_warranty_info(warranty_info):
    cleaned_warranty_info = [
        'Service Tag', 
        'Model', 
        'Ship Date', 
        'Entitlement Type', 
        'Entitlement Start Date', 
        'Entitlement End Date', 
        'Entitlement Description'
        ]
    for item in warranty_info:
        service_tag = item.get('serviceTag')
        model = item.get('productLineDescription')
        ship_date = format_date(item.get('shipDate'))
        for entitlement in item.get('entitlements', []):
            cleaned_warranty_info.append([
                service_tag,
                model,
                ship_date,
                entitlement.get('entitlementType'),
                format_date(entitlement.get('startDate')),
                format_date(entitlement.get('endDate')),
                entitlement.get('serviceLevelDescription')
            ])
    return cleaned_warranty_info

def clean_asset_header_info(warranty_info):
    cleaned_asset_header_info = [
        'Service Tag', 
        'ID', 
        'Product Line', 
        'Ship Date'
        ]
    for item in warranty_info:
        service_tag = item.get('serviceTag')
        product_line = item.get('productLineDescription')
        ship_date = format_date(item.get('shipDate'))
        entry_id = item.get('id')
        cleaned_asset_header_info.append([
            service_tag,
            entry_id,
            product_line,
            ship_date
            ])
    return cleaned_asset_header_info

def read_asset_tags_from_sheet():
    """
    Read a list of domains from a specified Google Sheets range.
    
    :param spreadsheet_id: The ID of the Google Spreadsheet.
    :param range_name: The range of cells to read from (e.g., 'Sheet1!A:A').
    :return: List of domains read from the sheet.
    """
    worksheetIndex = 1
    sheetIndex = 62
    
    try:
        # Get the values from the sheet
        results = gs.read_sheet(worksheetIndex, sheetIndex)
        #print(results)

        # Check if there is any data
        if not results:
            print("No data found.")
            return []

        # Extract domains from the values list
        service_tags = [col[0] for col in results if col]  # Assuming domains are in the first [0] column
        #print(domains)
        return service_tags[1:] # Skip the header row
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
def get_service_tags():
    service = "warranty"
    jwt = get_access_token(service)
    
    service_tags_url = 'https://apigtwb2c.us.dell.com/support/v2/service_tags'
    
    assets_url = 'https://apigtwb2c.us.dell.com/support/v2/assets'
    
    headers = {
        'Authorization': f'Bearer {jwt}',
        'Content-Type': 'application/json'
    }
    response = requests.get(service_tags_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to retrieve service tags: {response.status_code} - {response.text}")

# Main execution
def main():
    test_tag = '8VWSFZ1'
    try:
        #results = get_credentials_dell_warranty_api()
        #results = get_access_token(service_name="warranty")
        #results = get_service_tags()
        results = get_asset_header_by_service_tag(test_tag)
        #results = get_warranty_info_by_service_tag(test_tag)
        #results = get_device_info_by_service_tag(test_tag)
        #results = read_asset_tags_from_sheet()
        pprint.pprint(results)

    except Exception as e:
        print(f"An error occurred: {e}")
        
        
if __name__ == '__main__':
    main()
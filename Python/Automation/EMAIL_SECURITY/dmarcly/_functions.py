### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###

#logging.basicConfig(filename='c:\\users\\bill.mcdonald_alpham\\Documents\\Python\\errors.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_service_dmarcly():
    # GRAB API KEY FOR DMARCLY
    with open(
        '.\\_SHARED_\\api_accounts.json',
        'r') as api_accounts:
        api_keys = json.load(api_accounts)
    api_token = api_keys['dmarcly'][0]['api_key']
    return api_token

def get_aggregate_by_domain(num_days):
    # Grab credentials
    try:
        #print("Grabbing authorization credentials...\n")
        api_token = get_service_dmarcly()
    except Exception as err:
        print(f"An error occurred establishing authorization credentials: {err}")
        return

    #region: Build URL for the API endpoint
    base_url = 'https://dmarcly.com/api/'
    function = 'aggregate_by_domain'
    url = f"{base_url}{function}"

    headers = {
        'Authorization': f'{api_token}',
        'Content-Type': 'application/json',
    }
    #pprint.pprint(json.dumps(headers))
    #endregion
    print(f"Num days = {num_days}")
    #region: Define request parameters
    requested_time_window = num_days # in days
    end_time = int(datetime.now().timestamp())
    start_time = int((datetime.now() - timedelta(days=requested_time_window)).timestamp())

    # Initialize parameters for the GET request
    params = {
        'start': start_time,
        'end': end_time,
        'page': 1,  # Start with the first page
        'per_page': 15,  # Adjust as per the API's limits
    }
    #endregion
    print(params)
    
    all_records = []  # List to store all records

    try:
        while True:
            # Make the request to the DMARCLY API with query parameters
            response = requests.get(url, headers=headers, params=params)

            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()
                records = data.get('records', [])
                all_records.extend(records)

                # Check if there are more pages to fetch
                if len(records) < params['per_page']:
                    # If fewer records returned than requested, assume last page
                    break

                # Increment the page number for the next request
                params['page'] += 1
            else:
                print(f"Failed to retrieve data: {response.status_code} {response.text}")
                return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
    results = [
        # Add header row here
        ['Domain', 'Volume', 'DMARC', 'DMARCUnaligned', 'DMARCUnalignedARCPass',
         'DKIMAligned', 'DKIM', 'DKIMFailed', 'SPFAligned', 'SPF', 'SPFFailed']
    ]
    for record in all_records:
        results.append([
            record.get('Domain', ''),
            record.get('Volume', ''),
            record.get('DMARC', ''),
            record.get('DMARCUnaligned', ''),
            record.get('DMARCUnalignedARCPass', ''),
            record.get('DKIMAligned', ''),
            record.get('DKIM', ''),
            record.get('DKIMFailed', ''),
            record.get('SPFAligned', ''),
            record.get('SPF', ''),
            record.get('SPFFailed', '')
        ])

    # Check and print the retrieved data
    num_records = len(all_records)
    print(f"Total number of records found: {num_records}")
    #print(results)
    #for record in all_records:
        #print(record)  # Print each record's details

    return results

def add_domain_to_dmarcly(domain):
    """
    Add a domain to the DMARCLY account using the DMARCLY API.
    
    :param domain: The domain name to be added.
    :return: Response from the DMARCLY API.
    """
    try:
        print("Grabbing authorization credentials...\n")
        api_token = get_service_dmarcly()
    except Exception as err:
        print(f"An error occurred establishing authorization credentials: {err}")
        return

    # API endpoint
    url = "https://dmarcly.com/api/add_domain"

    # Headers for the request
    headers = {
        'Authorization': f'{api_token}',
        'Content-Type': 'application/x-www-form-urlencoded',  # Use URL-encoded form data
    }

    # Data to be sent in the PUT request
    data = {
        'domain': domain
    }

    try:
        # Send the PUT request to the DMARCLY API
        response = requests.put(url, headers=headers, data=data)

        # Check if the request was successful
        if response.status_code == 200:
            print(f"{domain} added successfully.")
            return response.json()
        else:
            print(f"Failed to add domain: {response.status_code} {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_domains_from_sheet(spreadsheet_id, range_name):
    """
    Read a list of domains from a specified Google Sheets range.
    
    :param spreadsheet_id: The ID of the Google Spreadsheet.
    :param range_name: The range of cells to read from (e.g., 'Sheet1!A:A').
    :return: List of domains read from the sheet.
    """
    # Example usage
    spreadsheet_id = '1di8Vo5tZU0KXm3RuFX18-XKz_nEwL-qxpgE6pFsWwjY'
    range_name = 'test_sheet!A6:A'  # Adjust the range as needed

    try:
        # Get the values from the sheet
        results = gs.read_sheet(spreadsheet_id, range_name).get('values', [])

        # Check if there is any data
        if not results:
            print("No data found.")
            return []

        # Extract domains from the values list
        domains = [row[0] for row in results if row]  # Assuming domains are in the first column

        return domains
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def process_domains(domain_list):
    """
    Read domains from a Google Sheet and add them to DMARCLY.
    
    :param spreadsheet_id: The ID of the Google Spreadsheet.
    :param range_name: The range of cells to read from (e.g., 'Sheet1!A:A').
    :param credentials_file: Path to the service account JSON file.
    """
    domains = domain_list
    
    if not domains:
        print("No domains to process.")
        return

    # Add each domain to DMARCLY
    for domain in domains:
        print(f"Adding domain: {domain}\n")
        result = add_domain_to_dmarcly(domain)
        
    
def main():
    try:
        print('Executing tasks...\n')
        
        
        # Example usage
        test_spreadsheet_index = 3
        test_range_name = 99
        
        try:
            print("Getting authorization for connecting to the spreadsheet...\n")
            result = gs.read_sheet(test_spreadsheet_index,test_range_name)
            #pprint.pprint(result)
        except Exception as err:
            print(f"An error occurred setting service credentials: {err}")

        #result = get_aggregate_by_domain()
        #result = add_domain_to_dmarcly('mytestdomain.com')
        
        #print(results)
        if result:
            print(f'Test: successful\n{result}')
    except Exception as err:
        print(f"Test: failure...\nAn error occurred getting list: {err}")

if __name__ == '__main__':
    main()

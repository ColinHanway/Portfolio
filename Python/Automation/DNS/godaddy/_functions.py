### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###


def get_godaddy_api():
    ### ACCESS JSON KEY FILE
    with open(
        '_SHARED_\\api_accounts.json',
        'r') as api_accounts:
        api_keys = json.load(api_accounts)
        # GET GODADDY API INFO
        api_key = api_keys['godaddy'][0]['api_key']
        api_secret = api_keys['godaddy'][0]['api_secret']
    return api_key, api_secret

def get_domain_names_list():
    api_key, api_secret = get_godaddy_api()
    """
    Get a list of domain names from GoDaddy API.

    Parameters:
    - api_key (str): Your GoDaddy API key.
    - api_secret (str): Your GoDaddy API secret.

    Returns:
    - list: A list of domain names.
    """
    url = 'https://api.godaddy.com/v1/domains'
    headers = {
        'Authorization': f'sso-key {api_key}:{api_secret}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        domains = response.json()
        domains = domains[:3]
        domain_names_list = [domain['domain'] for domain in domains]
        return domain_names_list
    else:
        print(f"Error fetching domain names: {response.status_code} {response.text}")
        return None
    
def get_active_godaddy_domains():
    api_key, api_secret = get_godaddy_api()
    #print(f"api_key: {api_key}, api_secret: {api_secret}")

    ### SET GODADDY CALL VARIABLE
    base_url = 'https://api.godaddy.com/'
    function = 'v1/domains'
    limit = 0
    page = 0 # START ON FIRST PAGE OF RESULTS
    per_page = 100 # MAX RESULTS AS DETERMINED BY TEST CALLS OR LIMITED TO REDUCE TIMEOUTS 
    total_results = 0
    total_pages = 2 # initial value >1 until PAGE 1 processes and gets actual count
    max_pages = 99
    # Parameters for pagination
    marker = ''  # start empty and then update with last domain of previous call loop
    last_domain = 'anydomain.com' # keep track of last domain in loop
    # includes
    inc_authcode = False
    inc_contacts = False
    inc_nameServers = False
    # statuses
    inc_active = False
    # status groups
    inc_visible = False
    inc_inactive = False
    inc_pre_registration = False
    inc_redemption = False
    inc_renewable = False
    inc_verification_icann = False

    ### BUILD GODADDY CALL
    # Construct the authorization header
    headers = {'Authorization': f'sso-key {api_key}:{api_secret}'}
    total_count = 0
    domains = []

    
    # Get the initial total pages count (assuming you have a way to determine this)
    total_pages = 10  # Set this to an appropriate initial value if not available
    
    with tqdm(total=total_pages, desc='Fetching Pages') as pbar:
        while page <= total_pages:
            # Construct the URL for the API endpoint
            url = f'{base_url}{function}?status=ACTIVE&statusGroups=&marker={marker}'
            
            # Send the GET request
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                # Handle successful response
                domain_list = response.json()
                pprint.pprint(domain_list[:1])
                return
                count = 0
                
                if marker == '':
                    domains.append(['Domain Name', 'Expires', 'Status'])
                
                # CONVERT RESPONSE TO GOOGLE SHEET COLUMNS AND APPEND IT TO ARRAY
                for each_domain in domain_list:
                    if each_domain['status'] == 'ACTIVE':
                        if 'expires' in each_domain:
                            formatted_date = datetime.strptime(each_domain['expires'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
                        else:
                            formatted_date = 'n/a'
                        domain = [each_domain['domain'], formatted_date, each_domain['status']]
                        domains.append(domain)
                        marker = each_domain['domain']  # Update marker for next loop
                    total_count += 1
                    count += 1
                
                # Update progress bar
                pbar.update(1)
                
                # Increment page counter
                page += 1
                
                if count < per_page:
                    break
                
            else:
                # Handle error response
                print(f"Request failed with status code: {response.status_code}")
                print(response.text)
                break
    
    return domains

def get_all_godaddy_domains():
    api_key, api_secret = get_godaddy_api()
    #print(f"api_key: {api_key}, api_secret: {api_secret}")

    ### SET GODADDY CALL VARIABLE
    base_url = 'https://api.godaddy.com/'
    function = 'v1/domains'
    limit = 0
    page = 0 # START ON FIRST PAGE OF RESULTS
    per_page = 100 # MAX RESULTS AS DETERMINED BY TEST CALLS OR LIMITED TO REDUCE TIMEOUTS 
    total_results = 0
    total_pages = 2 # initial value >1 until PAGE 1 processes and gets actual count
    max_pages = 99
    # Parameters for pagination
    marker = ''  # start empty and then update with last domain of previous call loop
    last_domain = 'anydomain.com' # keep track of last domain in loop
    # includes
    inc_authcode = False
    inc_contacts = False
    inc_nameServers = False
    # statuses
    inc_active = False
    # status groups
    inc_visible = False
    inc_inactive = False
    inc_pre_registration = False
    inc_redemption = False
    inc_renewable = False
    inc_verification_icann = False

    ### BUILD GODADDY CALL
    # Construct the authorization header
    headers = {'Authorization': f'sso-key {api_key}:{api_secret}'}
    total_count = 0
    domains = []

    
    # Get the initial total pages count (assuming you have a way to determine this)
    total_pages = 10  # Set this to an appropriate initial value if not available
    
    with tqdm(total=total_pages, desc='Fetching Pages') as pbar:
        while page <= total_pages:
            # Construct the URL for the API endpoint
            url = f'{base_url}{function}?marker={marker}'
            
            # Send the GET request
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                # Handle successful response
                domain_list = response.json()
                count = 0
                
                if marker == '':
                    domains.append(['Domain Name', 'Expires', 'Status'])
                
                # CONVERT RESPONSE TO GOOGLE SHEET COLUMNS AND APPEND IT TO ARRAY
                for each_domain in domain_list:
                    if 'expires' in each_domain:
                        formatted_date = datetime.strptime(each_domain['expires'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
                    else:
                        formatted_date = 'n/a'
                    domain = [each_domain['domain'], formatted_date, each_domain['status']]
                    domains.append(domain)
                    marker = each_domain['domain']  # Update marker for next loop
                    total_count += 1
                    count += 1
                
                # Update progress bar
                pbar.update(1)
                
                # Increment page counter
                page += 1
                
                if count < per_page:
                    break
                
            else:
                # Handle error response
                print(f"Request failed with status code: {response.status_code}")
                print(response.text)
                break

    return domains

def get_godaddy_dns_records(domain):
    api_key, api_secret = get_godaddy_api()

    """
    Fetch all DNS records for a domain using the GoDaddy API.

    Parameters:
    - domain (str): The domain to look up (e.g., 'example.com').
    - api_key (str): Your GoDaddy API key.
    - api_secret (str): Your GoDaddy API secret.

    Returns:
    - list: A list of DNS records if successful.
    - None: If the request fails.
    """
    url = f'https://api.godaddy.com/v1/domains/{domain}/records'
    headers = {'Authorization': f'sso-key {api_key}:{api_secret}'}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching DNS records: {response.status_code} {response.text}")
        return None
    
def get_all_domains_records(domains_list):
    api_key, api_secret = get_godaddy_api()
    """
    Process each domain in the list to get and convert DNS records.

    Parameters:
    - domains (list): A list of domain names to process.
    - api_key (str): Your GoDaddy API key.
    - api_secret (str): Your GoDaddy API secret.

    Returns:
    - list: A list of lists with the domain name included in each record.
    """
    all_records = []
    
    for domain in domains_list:
        print(f"Processing domain: {domain}")
        dns_records = get_godaddy_dns_records(domain)
        
        if dns_records:
            # Convert DNS records to a list of lists
            domain_records = convert_dns_records_to_list(dns_records)
            
            # Add domain name to each record
            for record in domain_records[1:]:  # Skip the header
                all_records.append([domain] + record)
    
    # Add header with domain name
    header = ['DOMAIN NAME'] + domain_records[0]
    all_records.insert(0, header)
    
    return all_records


def get_godaddy_domain_info(domain):
    api_key, api_secret = get_godaddy_api()

    """
    Fetch all DNS records for a domain using the GoDaddy API.

    Parameters:
    - domain (str): The domain to look up (e.g., 'example.com').
    - api_key (str): Your GoDaddy API key.
    - api_secret (str): Your GoDaddy API secret.

    Returns:
    - list: A list of DNS records if successful.
    - None: If the request fails.
    """
    url = f'https://api.godaddy.com/v1/domains/{domain}'
    headers = {'Authorization': f'sso-key {api_key}:{api_secret}'}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching DNS records: {response.status_code} {response.text}")
        return None
    
def convert_dns_records_to_list(dns_records):
    """
    Convert a list of DNS record dictionaries to a list of lists with a specific header.

    Parameters:
    - dns_records (list): A list of dictionaries representing DNS records.

    Returns:
    - list: A list of lists where each inner list represents a DNS record with the header
            ['TYPE', 'DATA', 'NAME', 'TTL'].
    """
    header = ['TYPE', 'DATA', 'NAME', 'TTL']
    records_list = [header]
    
    for record in dns_records:
        records_list.append([record['type'], record['data'], record['name'], record['ttl']])
    
    return records_list

    
def main():
    
    #results = get_godaddy_api()
    #pprint.pprint(results)
    domain = 'payalphamedia.com'
    #results = get_godaddy_domain_info(domain)
    #pprint.pprint(results)
    results = get_active_godaddy_domains()
    #results = get_domain_names_list()
    #results = results
    #results = get_all_domains_records(results)
    #results = get_godaddy_dns_records(domain)
    #results = convert_dns_records_to_list(results)
    #pprint.pprint(results)
    print(f"Successfully tested")
        

if __name__ == '__main__':
    main()

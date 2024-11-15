### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.auth import HTTPBasicAuth

api_name = "zendesk"
subdomain = "alphamedia"
email = "bill.mcdonald@alphamediausa.com"
title = "Zendesk"


def get_credentials():  # Added api_name as parameter for flexibility
    # Load API credentials from the file
    file_path = os.path.join('_PRIVATE_', 'api_accounts.json')
    with open(file_path, 'r') as api_accounts:
        api_keys = json.load(api_accounts)
    
    # Extract credentials based on the provided API name
    token = api_keys[api_name][0]["api_token"]
    return token

def get_all_end_users():
    """
    Fetches all end-users from Zendesk API.

    Args:
    - subdomain (str): Your Zendesk subdomain (e.g., 'yourcompany').
    - api_token (str): Your Zendesk API token.
    - email (str): The email address associated with your Zendesk account.

    Returns:
    - list: A list of dictionaries representing the end-users.
    """
    
    api_token = get_credentials()
    
    url = f'https://{subdomain}.zendesk.com/api/v2/users.json'
    auth = HTTPBasicAuth(f'{email}/token', api_token)

    users = []
    page_urls = [url]
    pages_fetched = 0
        
    with tqdm(desc='Fetching Pages', unit='page') as pbar:
        while page_urls:
            page_url = page_urls.pop(0)
            response = requests.get(page_url, auth=auth)
            if response.status_code == 401:
                raise Exception("Unauthorized: Check your email and API token.")
            response.raise_for_status()
            data = response.json()
            users.extend(data.get('users', []))
            next_page = data.get('next_page')
            if next_page:
                # Ensure the next_page URL is a full URL
                if not next_page.startswith('http'):
                    next_page = f'https://{subdomain}.zendesk.com{next_page}'
                page_urls.append(next_page)

            pages_fetched += 1
            pbar.update(1)  # Update progress bar for each page fetched

    print(f"Total pages fetched: {pages_fetched}")
    print(f"Total users fetched: {len(users)}")
    #save_data_to_file(data, title, expiration_seconds=86400)
    #pprint.pprint(users[:5])
    return users

def filter_suspended_users(users):
    """
    Filters the list of users to include only those who are suspended.

    Args:
    - users (list): A list of dictionaries representing the users.

    Returns:
    - list: A filtered list of dictionaries representing suspended users.
    """
    suspended_users = [user for user in users if user.get('suspended') == True]
    print(f"Suspended users found: {len(suspended_users)}")
    return suspended_users

def get_all_end_users_and_ticket_counts():
    users = get_all_end_users()
    results = get_users_with_ticket_counts(users)
    return results

def get_user_id_by_email(email_address):
    api_token = get_credentials()

    url = f"https://{subdomain}.zendesk.com/api/v2/users/search.json?query={email_address}"
    response = requests.get(url, auth = HTTPBasicAuth(f'{email}/token', api_token))

    if response.status_code == 200:
        data = response.json()
        #print(f"Response JSON: {data}")  # Debugging line to see the full response
        
        if 'users' in data and isinstance(data['users'], list):
            if data['count'] > 0:
                user = data['users'][0]
                user_id = user.get('id')
                #print(f"User ID: {user_id}")
                if isinstance(user_id, int):
                    return user_id
                else:
                    print(f"Unexpected data type for user ID: {type(user_id)}")
                    return None
            else:
                print(f"No user found with email: {email_address}")
                return None
        else:
            print(f"Unexpected response structure: {data}")
            return None
    else:
        print(f"Failed to retrieve user ID. Status code: {response.status_code}, Response: {response.text}")
        return None

def delete_user(user_id):
    api_token = get_credentials()

    url = f"https://{subdomain}.zendesk.com/api/v2/users/{user_id}.json"
    response = requests.delete(url, auth = HTTPBasicAuth(f'{email}/token', api_token))
    if response.status_code == 204:
        print(f"User with ID {user_id} deleted successfully.")
    else:
        print(f"Failed to delete user with ID {user_id}. Status code: {response.status_code}")
        
def format_for_google_sheets(user_data):
    """
    Converts user data into a format suitable for Google Sheets with headers and rows.

    Args:
    - user_data (list of dict): List of user data dictionaries.

    Returns:
    - tuple: A tuple containing headers (list) and rows (list of lists).
    """
    
    users = []
    # Define headers based on expected user data structure
    headers = [
        "id", "url", "name", "email", "created_at", "updated_at", 
        "time_zone", "iana_time_zone", "phone", "shared_phone_number", 
        "locale_id", "locale", "organization_id", "role", 
        "verified", "external_id", "alias", "active", 
        "shared", "shared_agent", "last_login_at", "two_factor_auth_enabled", 
        "signature", "details", "notes", "role_type", "custom_role_id", 
        "moderator", "ticket_restriction", "only_private_comments", 
        "restricted_agent", "suspended", "default_group_id", 
        "report_csv"
    ]

    users.append(headers)

    for user in user_data:
        row = [
            user.get("id", ""),
            user.get("url", ""),
            user.get("name", ""),
            user.get("email", ""),
            user.get("created_at", ""),
            user.get("updated_at", ""),
            user.get("time_zone", ""),
            user.get("iana_time_zone", ""),
            user.get("phone", ""),
            user.get("shared_phone_number", ""),
            user.get("locale_id", ""),
            user.get("locale", ""),
            user.get("organization_id", ""),
            user.get("role", ""),
            user.get("verified", ""),
            user.get("external_id", ""),
            user.get("alias", ""),
            user.get("active", ""),
            user.get("shared", ""),
            user.get("shared_agent", ""),
            user.get("last_login_at", ""),
            user.get("two_factor_auth_enabled", ""),
            user.get("signature", ""),
            user.get("details", ""),
            user.get("notes", ""),
            user.get("role_type", ""),
            user.get("custom_role_id", ""),
            user.get("moderator", ""),
            user.get("ticket_restriction", ""),
            user.get("only_private_comments", ""),
            user.get("restricted_agent", ""),
            user.get("suspended", ""),
            user.get("default_group_id", ""),
            user.get("report_csv", ""),
        ]
        users.append(row)

    return users

def get_tickets_by_user_id(user_id):
    api_token = get_credentials()

    tickets = []
    url = f"https://{subdomain}.zendesk.com/api/v2/users/{user_id}/tickets/requested.json"
    
    while url:
        response = requests.get(url, auth=HTTPBasicAuth(f'{email}/token', api_token))
        
        if response.status_code == 200:
            data = response.json()
            tickets.extend(data.get('tickets', []))
            url = data.get('next_page')  # Pagination handling
        else:
            print(f"Failed to retrieve tickets for user {user_id}. Status code: {response.status_code}, Response: {response.text}")
            return []
    
    return tickets

def count_unclosed_tickets(user_id, retries=5):
    api_token = get_credentials()

    url = f'https://{subdomain}.zendesk.com/api/v2/search.json?query=type:ticket requester_id:{user_id} status<solved'
    for i in range(retries):
        try:
            response = requests.get(url, auth=HTTPBasicAuth(f'{email}/token', api_token))
            response.raise_for_status()
            return response.json()['count']
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
                time.sleep(retry_after)
            else:
                raise e
    raise Exception(f"Failed to get unclosed tickets for user {user_id} after {retries} retries.")

def process_user(user):
    unclosed_tickets = count_unclosed_tickets(user['id'])
    return [user['id'], user['name'], user['email'], unclosed_tickets]

def get_users_with_ticket_counts(users, max_workers=5):
    user_data = []
    headers = ['ID',"User", "Email", "Tickets"]
    user_data.append(headers)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_user, user): user for user in users}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing Users", unit="user"):
            user_data.append(future.result())
    return user_data            
def main():
    try:
        user_id = 5230789175451
        email_address = 'amy.reed@alphameidausa.com'
        print('Testing function...\n')
        #results = get_credentials()
        #results = get_zone_id('1009theeagle.com')
        #results = get_dns_records(results)
        #results = transform_dns_records_for_sheets(results)
        #results = get_all_end_users()
        users = get_all_end_users()
        results = get_users_with_ticket_counts(users[:5])
        #results = get_user_id_by_email(email_address)
        #results = get_tickets_by_user_id(user_id)
        #results = delete_user(user_id)
        #results = format_for_google_sheets(results[:2])
        pprint.pprint(results[:3])
        #pprint.pprint(results)
        print('Test: Success\n')
    except Exception as err:
        print(f"Test: Failure\n{err}")

if __name__ == '__main__':
    main()

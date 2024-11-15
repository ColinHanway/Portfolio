### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###


def get_credentials(): # Get auth info from file
    with open(
        '_PRIVATE_\\api_accounts.json', 'r'
        ) as api_accounts:
        api_keys = json.load(api_accounts)
    client_id = api_keys['adobe user management'][0]["client_id"]
    client_secret  = api_keys['adobe user management'][0]["client_secret"]
    org_id  = api_keys['adobe user management'][0]["org_id"]
    return client_id,client_secret, org_id

def get_access_token(): # Config Data
    client_id,client_secret, org_id = get_credentials()
    url = 'https://ims-na1.adobelogin.com/ims/token/v3'

    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'openid,AdobeID,user_management_sdk'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        token = response.json().get('access_token')
        #print('Access token:', token)
        return token, client_id, org_id
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

def get_all_users():
    """
    Retrieve all users from Adobe's User Management API.

    Args:
        access_token (str): The access token obtained from Adobe.

    Returns:
        dict: The JSON response containing user information or an error message.
    """
    
    access_token, api_key, org_id = get_access_token()
    
    users = []
    page = 0
    
    while True:
        url = f'https://usermanagement.adobe.io/v2/usermanagement/users/{org_id}/{page}'
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'X-Api-Key': api_key
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            # Add users from the current page to the list
            users.extend(data.get('users', []))
            
            # Check if there are more pages
            if data.get('has_more', False):
                page += 1
            else:
                break
        
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            print(f'Response content: {response.text}')
            users = f"error: {response.status_code}"
            break
        except Exception as err:
            print(f'Other error occurred: {err}')
            users = f"error: {response.status_code}"
            break
        
    save_data_to_file(users,"adobeUsersByGroup")

    return users
def get_all_users():
    """
    Retrieve all users from Adobe's User Management API.

    Args:
        access_token (str): The access token obtained from Adobe.

    Returns:
        dict: The JSON response containing user information or an error message.
    """
    
    access_token, api_key, org_id = get_access_token()
    
    users = []
    page = 0
    
    while True:
        url = f'https://usermanagement.adobe.io/v2/usermanagement/users/{org_id}/{page}/'
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'X-Api-Key': api_key
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            # Add users from the current page to the list
            users.extend(data.get('users', []))
            
            # Check if there are more pages
            if data.get('has_more', False):
                page += 1
            else:
                break
        
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            print(f'Response content: {response.text}')
            users = f"error: {response.status_code}"
            break
        except Exception as err:
            print(f'Other error occurred: {err}')
            users = f"error: {response.status_code}"
            break
        
    save_data_to_file(users,"adobeUsersByGroup")

    return users

def get_users_by_group():
    access_token, api_key, org_id = get_access_token()
    page = 0
    all_users = []
    
    while True:
        url = f'https://usermanagement.adobe.io/v2/usermanagement/users/{org_id}/{page}/'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'X-Api-Key': org_id
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if not data:  # No more data
                break
            
            all_users.extend(data.get('users', []))  # Add users to the list
            page += 1  # Move to the next page
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)
            break

    return all_users

def main():
    try:
        #results = get_credentials()
        #results = get_access_token()
        results = get_users_by_group()
        pprint.pprint(results[:2])

    except Exception as e:
        print(f"An error occurred: {e}")
        
        
if __name__ == '__main__':
    main()
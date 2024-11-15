### GLOBAL IMPORTS ###
#
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *
#
#####################

### LOCAL IMPORTS ###
#

#
#####################

api_name = "google"

def set_workspace_admin_credentials():
    try:
        # Path to your service account key file
        keyfile_path = '_SHARED_/service_account_key.json'
        
        # Scopes required for the API
        scopes = [
            'https://www.googleapis.com/auth/admin.directory.user',
            'https://www.googleapis.com/auth/admin.directory.user.alias.readonly',
            'https://www.googleapis.com/auth/admin.directory.group.readonly',
            'https://www.googleapis.com/auth/admin.directory.domain.readonly',
            'https://www.googleapis.com/auth/gmail.settings.basic',
            'https://www.googleapis.com/auth/spreadsheets'
        ]
        
        # Authentication using the service account key file
        credentials = Credentials.from_service_account_file(keyfile_path, scopes=scopes)
        
        # Build the service object for the Admin SDK Directory API
        service_workspace = build('admin', 'directory_v1', credentials=credentials)
        
        return service_workspace
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None    

def set_vault_admin_credentials():
    try:
        # Path to your service account key file
        keyfile_path = '_SHARED_/service_account_key.json'
        
        # Scopes required for the API
        scopes = [
            'https://www.googleapis.com/auth/ediscovery.readonly'
        ]
        
        # Authentication using the service account key file
        credentials = Credentials.from_service_account_file(keyfile_path, scopes=scopes)

    
        # Build the service object for the Admin SDK Directory API
        service_vault = build('vault', 'v1', credentials=credentials)
        
        return service_vault
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None    

def set_gmail_admin_credentials():
    try:
        # Path to your service account key file
        keyfile_path = '_SHARED_/service_account_key.json'
        
        # Scopes required for the API
        scopes = [
            'https://www.googleapis.com/auth/gmail.settings.basic'
            ]
        
        # Authentication using the service account key file
        credentials = Credentials.from_service_account_file(keyfile_path, scopes=scopes)
        
        # Use AuthorizedSession for authorization
        authed_session = AuthorizedSession(credentials)
        
        # Build the service object for the Admin SDK Directory API
        gmail_service = build('gmail', 'v1', credentials=credentials)
        
        return gmail_service
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None    
    
# GOOGLE SHEETS CREDENTIALS
def set_google_sheets_credentials():
    try:
        # Path to your service account key file
        # Construct the path to the JSON file
        file_path = os.path.join('..', '_PRIVATE_', 'api_accounts.json')
        # Read the credentials from the JSON file
        with open(file_path, 'r') as file:
            credentials = json.load(file)
            with open(file_path, 'r') as api_accounts:
                api_keys = json.load(api_accounts).get(api_name)
            api_keys = api_keys[0]

    except Exception as e:
        print(f"Error: Could not retrieve Google Sheets credentials")
        return None    
        
    # Scopes required for the API
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets'
    ]
        
    try:
        # Authentication using the service account key file
        credentials = Credentials.from_service_account_info(api_keys, scopes=scopes)
        service_sheets = build('sheets', 'v4', credentials=credentials)
        #print(credentials)
        return service_sheets

    except Exception as e:
        print(f"Error: {e}")
        return None    

def set_wide_orbit_traffic_credentials():
    try:
        # Path to your service account key file
        keyfile_path = './_SHARED_/api_accounts.json'
        
        with open(keyfile_path, 'r') as file:
                credentials = json.load(file)
            
        return credentials['wide_orbit_traffic'][0]
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None    

"""
credentials = set_google_sheets_credentials()
directory_service = build('admin', 'directory_v1', credentials=credentials)
sheets_service = build('sheets', 'v4', credentials=credentials)
gmail_service = build('gmail', 'v1', credentials=credentials)
"""
def main():
    try:
        print('Gathering...\n')
        service = set_google_sheets_credentials()
        #print(service)

        results = service
        #users = results.get('users', [])

        #pprint.pprint(users)
        print('successful test')
    except Exception as err:
        print(f"An error occurred getting list: {err}")

if __name__ == '__main__':
    main()

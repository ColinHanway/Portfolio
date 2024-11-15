### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, parse_qs
import webbrowser
from requests.auth import HTTPBasicAuth


api_name = "logmein"
company_id = ""
url_machines = "https://api.getgo.com/G2A/rest/v1/companies/{company_id}/machines"
url_groups = "https://api.getgo.com/G2A/rest/v1/companies"

def get_credentials():  # Added api_name as parameter for flexibility
    # Load API credentials from the file
    file_path = os.path.join('_PRIVATE_', 'api_accounts.json')
    with open(file_path, 'r') as api_accounts:
        api_keys = json.load(api_accounts)
    
    # Extract credentials based on the provided API name
    client_id = api_keys[api_name][0]["client_id"]
    client_secret = api_keys[api_name][0]["client_secret"]
    redirect_uri = api_keys[api_name][0]["redirect_uri"]
    auth_code = api_keys[api_name][0]["auth_code"]
    
    return client_id, client_secret, redirect_uri, auth_code

def open_authorization_url(client_id, redirect_uri):
    # Construct the authorization URL
    authorization_url = (
        f"https://authentication.logmeininc.com/oauth/authorize"
        f"?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}"
    )
    
    # Open the URL in the default web browser
    webbrowser.open(authorization_url)
    print(f"Opened URL: {authorization_url}")

    # Wait for user to authorize and capture the URL (manual step)
    print("Please authorize the application and copy the redirect URL.")
    print("Paste the redirect URL here:")

    # Manually input the redirect URL
    redirect_url = input("Redirect URL: ")
    
    return redirect_url

def get_access_token():
    client_id, client_secret, redirect_uri, authorization_code = get_credentials()
    token_url = "https://authentication.logmeininc.com/oauth/token"
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    payload = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri
    }
    
    auth = HTTPBasicAuth(client_id, client_secret)
    
    response = requests.post(token_url, headers=headers, data=payload, auth=auth)
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data.get('access_token')
    else:
        print(f"Failed to get token: {response.status_code} {response.text}")
        return None
    
def extract_code_from_url(redirect_url):
    parsed_url = urlparse(redirect_url)
    query_params = parse_qs(parsed_url.query)
    authorization_code = query_params.get('code', [None])[0]
    return authorization_code

def get_authorization_code():
    client_id, client_secret, redirect_uri, auth_code = get_credentials()

    redirect_url = open_authorization_url(client_id, redirect_uri)
    authorization_code = extract_code_from_url(redirect_url)

    return authorization_code

def get_companies():
    access_token = get_access_token()
    
    conn = http.client.HTTPSConnection("api.getgo.com")

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    
    conn.request("GET", "/G2A/rest/v1/companies?q=my%20device%20group&offset=1&limit=25&sortField=companyId&sortOrder=desc", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
    
def get_machines(api_key, company_id):
    url = f"https://api.getgo.com/G2A/rest/v1/companies/{company_id}/machines"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        machines = response.json()
        return machines
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
def main():
    try:
        print('Testing function...\n')
        #results = get_credentials()
        results = get_authorization_code()
        #results = get_access_token()
        #results = get_companies()
        #print(results)
        print('Test: Success\n')
        pprint.pprint(results[:2])
    except Exception as err:
        print(f"Test: Failure\n{err}")

if __name__ == '__main__':
    main()

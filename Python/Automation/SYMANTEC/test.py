import requests, json, pprint, datetime
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session


# API endpoints
token_url = 'https://api.sep.securitycloud.symantec.com/v1/oauth2/tokens'
devices_url = 'https://api.sep.securitycloud.symantec.com/v1/devices'

# Authentication (replace with your credentials and scopes)
with open(
    'api_accounts.json',
    'r') as api_accounts:
    api_keys = json.load(api_accounts)
    #client_id = api_keys['symantec'][0]
    #client_secret = api_keys['symantec'][1]
    
    #print(client_id)

# Credentials
client_id = 'O2ID.RG0D9lsbSzm0Sm3KiLSCeg.WSzmMVKLTByNN-P2EOusdw.6r6e6dffkoe45eos0dvfmf3us0'
client_secret = '1terudqmvb4vd6p8crl9qtkrg116gsrbh1j'

date_of_export = datetime.date.today().strftime("%Y-%m-%d")
last_export_date = date_of_export
count = 0


def get_access_token():
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
        
access_token = get_access_token()

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}
params = {
    'limit': 10  # Limiting to 10 results
}
response = requests.get(devices_url, headers=headers, params=params)

if response.status_code == 200:
    devices = response.json()
else:
    print(f'Failed to fetch device information: {response.status_code} - {response.text}')

# Main execution
if access_token:
#    print('test')
    device_info = devices
    pprint.pprint(device_info)
    
else:
    print('Unable to fetch device information.')


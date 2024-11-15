import json

def get_keys(provider):
    with open(
    '.\\api_accounts.json',
    'r') as api_accounts:
        api_keys = json.load(api_accounts)
        
        api_key = api_keys[provider][0]['api_key']
        api_secret = api_keys[provider][0]['api_secret']

        return api_key, api_secret

import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '_GITHUB_')))
from _SHARED_._common_imports import *

from zeep import Client # Python SOAP client for NetSuite
from zeep.wsse.signature import Signature
from zeep.wsse.username import UsernameToken

def get_service_netsuite():

    # WSDL URL
    wsdl = 'https://webservices.netsuite.com/wsdl/v2021_1_0/netsuite.wsdl'

    # Create a Zeep client
    client = Client(wsdl=wsdl)

    # Authentication setup
    client.service.login(
        email='your_email@example.com',
        password='your_password',
        account='your_account_id',
        role={'internalId': 'your_role_id'}
    )

    # Perform a search for fixed assets
    search = client.service.search(
        searchRecord={
            'recordType': 'fixedAsset',
            'searchType': 'Advanced',
            'criteria': {
                'basic': {
                    'type': 'searchStringField',
                    'operator': 'contains',
                    'searchValue': 'your_search_value'
                }
            }
        }
    )

    # Process the search results
    for record in search['recordList']['record']:
        print(record)


def main():
    try:
        #print('Gathing a list...\n')
        results = get_service_netsuite()
        #results = get_users()
        #results = get_users_summary()
        #results = get_groups()
        #results = get_auto_forwarding_settings()
        #results = get_domain_list()
        #results = get_domain_list()
        #print(results)
        print('successful test')
    except Exception as err:
        print(f"An error occurred getting list: {err}")

if __name__ == '__main__':
    main()

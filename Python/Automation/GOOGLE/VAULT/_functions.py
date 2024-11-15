### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###

service = gw.get_service_vault()

user_email = 'bill.mcdonald@alphamediausa.com'

def gam_get_matters_for_user(user_email):
    command = f'gam user {user_email} vault matters'

def parse_open_matter_ids(csv_data):
    """Parse the CSV data and return a list of matterIDs where the state is 'open'."""
    matter_ids = []
    reader = csv.DictReader(csv_data.splitlines())
    
    for row in reader:
        if row['state'].lower() == 'open':
            matter_ids.append(row['matterId'])
    
    return matter_ids
            
def process_matter_details(matter_details):
    # Ensure matter_details is in the form of a list of lists
    if not isinstance(matter_details, list) or not all(isinstance(i, list) for i in matter_details):
        raise ValueError("matter_details should be a list of lists")

    # Extract headers and rows
    headers = matter_details[0]
    rows = matter_details[1:]
    
    processed_data = []

    for row_index, row in enumerate(rows):
        matter_dict = {}
        accounts = []
        i = 0
        
        # Process standard fields before accounts
        while i < len(headers):
            header = headers[i]
            try:
                if header.startswith('accounts'):
                    break
                matter_dict[header] = row[i] if i < len(row) else None
                i += 1
            except IndexError:
                print(f"IndexError processing standard fields in row {row_index}: headers={headers}, row={row}")
                break  # Stop processing this row if there's an index error
        
        # Process accounts fields
        current_account = {}
        while i < len(headers):
            try:
                if headers[i].startswith('accounts'):
                    account_idx = headers[i].split('.')[1]  # Extract account index
                    if not account_idx.isdigit():
                        break
                    
                    # Initialize account if it doesn't exist
                    while len(accounts) <= int(account_idx):
                        accounts.append({})
                    
                    account_key = headers[i].split('.', 2)[-1]  # Extract field key for account
                    if i < len(row):
                        accounts[int(account_idx)][account_key] = row[i]
                    else:
                        accounts[int(account_idx)][account_key] = None  # Handle missing data
                i += 1
            except IndexError:
                print(f"IndexError processing account fields in row {row_index}: headers={headers}, row={row}")
                break  # Stop processing account fields for this row
        
        # Assign processed accounts data to the matter dictionary
        matter_dict['accounts'] = accounts
        processed_data.append(matter_dict)
    
    return processed_data

def list_matters():
    try:
        # Request to get a list of all matters
        results = service.matters().list().execute()
        pprint.pprint(results)
        # Get the list of matters
        matters = results.get('matters', [])
        
        if not matters:
            print('No matters found.')
        else:
            print('Matters:')
            for matter in matters:
                print(f"Name: {matter['name']}, Matter ID: {matter['matterId']}, State: {matter['state']}")

    except HttpError as error:
        print(f"An HTTP error occurred: {error}")
    except AttributeError as error:
        print(f"An AttributeError occurred: {error}")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():

    try:
        result = list_matters()        
        print(result[:3])

    except Exception as err:
        print(f"An error occurred testing: {err}")

if __name__ == '__main__':
    main()

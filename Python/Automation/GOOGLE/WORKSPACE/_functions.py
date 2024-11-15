### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess

customer_id = 'C02wg51jy'

def run_gam_command(command):
    try:
        # Run the gam command and capture the output
        print(f"Running GAM command: {command}")
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"Error: {result.stderr}")
            return None
    except Exception as e:
        print(f"An exception occurred: {e}")
        return None

def process_gam_output(output):
    # Example processing function
    lines = output.splitlines()
    # Process each line as needed, for example, parsing CSV lines
    for line in lines:
        print(line)  # Replace with your processing logic
        
def get_service_workspace():
    try:
        service = gauth.set_workspace_admin_credentials()
        #print(f"Workspace service created: {service}")
    except Exception as err:
        print(f"An error occurred setting service credentials: {err}")
        
    return service

def get_service_vault():
    try:
        service = gauth.set_vault_admin_credentials()
        #print(f"Workspace service created: {service}")
    except Exception as err:
        print(f"An error occurred setting service credentials: {err}")
        
    return service
# Retrieve user data (adjust parameters as needed)
def get_users():
    service = get_service_workspace()
    
    users = []
    page_token = None
    while True:
        results = service.users().list(customer=customer_id, maxResults=500, pageToken=page_token).execute()
        users.extend(results.get('users', []))
        page_token = results.get('nextPageToken')
        if not page_token:
            break
    return users

def get_user(email_address):
    service = get_service_workspace()
    
    results = service.users().get(userKey=email_address).execute()
    return results

def get_users_summary():
    users = get_users()

    user_list = []
    headers = ['="First Name ("&COUNTA(A7:A)&")"',
            'Last Name',
            'Primary Email',
            'OU',
            'Suspended',
            'Last Login',
            'Recovery Email',
            'Employee ID',
            'Employee Type',
            'Employee Title',
            'Employee Department',
            'Manager Email',
            '2SV Enrolled',
            '2SV Enforced',
            'Admin',
            'Delegated Admin',
            'Change Password at next login',
            'Created',
            'Archived'
            ]
    user_list.append(headers)

    for user in tqdm(users, desc="Processing users", unit="user"):
        employeeId = ''
        for external_id in user.get('externalIds', []):
            if "type" in external_id and external_id["type"] == "organization" and external_id["value"] != '':
                employeeId = external_id["value"]
                break  # Exit the loop once employee ID is found

        recoveryEmail = user.get('recoveryEmail', '')

        employeeTitle = ''
        employeeDepartment = ''
        employeeType = ''
        for organization in user.get('organizations', []):
            if 'title' in organization:
                employeeTitle = organization['title']
            if 'department' in organization:
                employeeDepartment = organization['department']
            if 'description' in organization:
                employeeType = organization['description']
            break  # Exit loop after finding the first organization

        managerEmail = ''
        for manager in user.get('relations', []):
            if 'type' in manager and manager['type'] == 'manager':
                managerEmail = manager['value']
            break  # Exit loop after finding the first manager

        # Parse the UTC datetime string
        utc_dateLastLogin_str = user['lastLoginTime']
        utc_dateLastLogin = parser.isoparse(utc_dateLastLogin_str)
        dateLastLogin = utc_dateLastLogin.astimezone()
        dateLastLogin = dateLastLogin.strftime("%Y-%m-%d")

        utc_dateCreated_str = user['creationTime']
        utc_dateCreated = datetime.fromisoformat(utc_dateCreated_str)
        dateCreated = utc_dateCreated.astimezone()
        dateCreated = dateCreated.strftime("%Y-%m-%d")
        
        isArchived = user['archived']

        each_record = [
            user['name']['givenName'],
            user['name']['familyName'],
            user['primaryEmail'],
            user['orgUnitPath'].lstrip("/"),
            user['suspended'],
            dateLastLogin,
            recoveryEmail,
            employeeId,
            employeeType,
            employeeTitle,
            employeeDepartment,
            managerEmail,
            user['isEnrolledIn2Sv'],
            user['isEnforcedIn2Sv'],
            user['isAdmin'],
            user['isDelegatedAdmin'],
            user['changePasswordAtNextLogin'],
            dateCreated,
            isArchived
        ]
        user_list.append(each_record)
    
    return user_list

def get_user_summary(email_address):
    users = get_user(email_address)

    user_list = []
    headers = ['="First Name ("&COUNTA(A7:A)&")"',
            'Last Name',
            'Primary Email',
            'OU',
            'Suspended',
            'Last Login',
            'Recovery Email',
            'Employee ID',
            'Employee Type',
            'Employee Title',
            'Employee Department',
            'Manager Email',
            '2SV Enrolled',
            '2SV Enforced',
            'Admin',
            'Delegated Admin',
            'Change Password at next login',
            'Created'
            ]
    user_list.append(headers)

    for user in tqdm(users, desc="Processing users", unit="user"):
        employeeId = ''
        for external_id in user.get('externalIds', []):
            if "type" in external_id and external_id["type"] == "organization" and external_id["value"] != '':
                employeeId = external_id["value"]
                break  # Exit the loop once employee ID is found

        recoveryEmail = user.get('recoveryEmail', '')

        employeeTitle = ''
        employeeDepartment = ''
        employeeType = ''
        for organization in user.get('organizations', []):
            if 'title' in organization:
                employeeTitle = organization['title']
            if 'department' in organization:
                employeeDepartment = organization['department']
            if 'description' in organization:
                employeeType = organization['description']
            break  # Exit loop after finding the first organization

        managerEmail = ''
        for manager in user.get('relations', []):
            if 'type' in manager and manager['type'] == 'manager':
                managerEmail = manager['value']
            break  # Exit loop after finding the first manager

        # Parse the UTC datetime string
        utc_dateLastLogin_str = user['lastLoginTime']
        utc_dateLastLogin = parser.isoparse(utc_dateLastLogin_str)
        dateLastLogin = utc_dateLastLogin.astimezone()
        dateLastLogin = dateLastLogin.strftime("%Y-%m-%d")

        utc_dateCreated_str = user['creationTime']
        utc_dateCreated = datetime.fromisoformat(utc_dateCreated_str)
        dateCreated = utc_dateCreated.astimezone()
        dateCreated = dateCreated.strftime("%Y-%m-%d")

        each_record = [
            user['name']['givenName'],
            user['name']['familyName'],
            user['primaryEmail'],
            user['orgUnitPath'].lstrip("/"),
            user['suspended'],
            dateLastLogin,
            recoveryEmail,
            employeeId,
            employeeType,
            employeeTitle,
            employeeDepartment,
            managerEmail,
            user['isEnrolledIn2Sv'],
            user['isEnforcedIn2Sv'],
            user['isAdmin'],
            user['isDelegatedAdmin'],
            user['changePasswordAtNextLogin'],
            dateCreated
        ]
        user_list.append(each_record)
    
    return user_list

    #pprint.pprint(user_list)
    
def get_groups_old():
    service = get_service_workspace()
    all_groups = []
    page_token = None

    while True:
        results_fetch_groups = service.groups().list(customer=customer_id, maxResults=500, pageToken=page_token).execute()
        groups = results_fetch_groups.get('groups', [])
        all_groups.extend(groups)
        page_token = results_fetch_groups.get('nextPageToken')
        if not page_token:
            break

    return all_groups

def get_user_aliases_old():
    service = get_service_workspace()
    
    try:
        user_list = get_users()
        print(f"All {len(user_list)} user aliases have been collected")
    except Exception as err:
        print(f"An error occurred getting users: {err}")
    
    user_aliases_list = []
    total_users_count = len(user_list)

    user_list = user_list[:10]

    with tqdm(total=total_users_count, desc="Fetching User Aliases") as pbar:
        for user in user_list:
            user_key = user['primaryEmail']
            
            # Fetch aliases for the user
            request = service.users().aliases().list(userKey=user_key)
            response = request.execute()
            
            # Process and collect aliases
            aliases = response.get('aliases', [])
            user_aliases_list.extend(aliases)
            
            pbar.update(1)  # Update progress bar with each processed user
    print(f"All user aliases have been processed")
    return user_aliases_list[:10]

def callback(request_id, response, exception):
    if exception is not None:
        print(f"Error in request {request_id}: {exception}")
    else:
        print(f"Response for request {request_id}: {response}")

def get_user_aliases_batch(batch_size=100):
    service = get_service_workspace()  # Ensure this returns a valid service object
    try:
        user_list = get_users()
        print(f"All user aliases have been collected")
    except Exception as err:
        print(f"An error occurred getting users: {err}")
        return []

    user_aliases_list = []

    def process_user(user_key):
        try:
            request = service.users().aliases().list(userKey=user_key).execute()
            user_aliases_list.append((user_key, request))
        except HttpError as err:
            print(f"An error occurred getting user aliases for user {user_key}: {err}")

    # Use tqdm to show progress for each chunk of users
    for i in tqdm(range(0, len(user_list), batch_size), desc="Processing user batches"):
        chunk = user_list[i:i + batch_size]
        for user in tqdm(chunk, desc="Processing individual users", leave=False):
            user_key = user['primaryEmail']
            process_user(user_key)
            
    #pprint.pprint(user_aliases_list)
            
    user_aliases = format_aliases_to_sheets(user_aliases_list)
    
    #pprint.pprint(user_aliases)
   

    return user_aliases

def format_aliases_to_sheets(aliases_list):
# Define the header row
    headers = ["ALIAS", "PRIMARY", "USER/GROUP", "ID", "ETAG"]

    # Initialize the list with the header row
    formatted_data = [headers]

    # Process each aliases_list entry
    for user_key, response in aliases_list:
        # Extract alias data
        for alias in response.get('aliases', []):
            kind = alias.get('kind', '')
            # Store 'USER' if kind is 'admin#directory#alias'
            user_group = 'USER' if kind == 'admin#directory#alias' else ''
            row = [
                alias.get('alias', ''),
                alias.get('primaryEmail', ''),
                user_group,  # Use user_group here
                alias.get('id', ''),
                alias.get('etag', '')
            ]
            formatted_data.append(row)

    return formatted_data

def get_group_aliases_old():
    service = get_service_workspace()
    
    group_aliases_list = []
    total_groups_count = 0
    page_token = None

    try:
        # Calculate total groups count
        while True:
            results_fetch_groups = service.groups().list(customer=customer_id, maxResults=500, pageToken=page_token).execute()
            groups = results_fetch_groups.get('groups', [])
            total_groups_count += len(groups)
            page_token = results_fetch_groups.get('nextPageToken')
            if not page_token:
                break
        
        print(f"Total groups to process: {total_groups_count}")

        # Process groups
        page_token = None  # Reset page_token for the second pass
        with tqdm(total=total_groups_count, desc="Fetching Group Aliases") as pbar:
            while True:
                results_fetch_groups = service.groups().list(customer=customer_id, maxResults=500, pageToken=page_token).execute()
                groups = results_fetch_groups.get('groups', [])
                for group in groups:
                    pbar.update(1)
                    group_key = group['email']
                    alias_results = service.groups().aliases().list(groupKey=group_key).execute()
                    group_aliases = alias_results.get('aliases', [])
                    for alias in group_aliases:
                        each_record = [
                            alias['alias'],
                            group_key,
                            "GROUP"
                        ]
                        group_aliases_list.append(each_record)
                page_token = results_fetch_groups.get('nextPageToken')
                if not page_token:
                    break

        print(f"All group aliases have been processed")

    except HttpError as error:
        print(f"An error occurred: {error}")
    return group_aliases_list

def get_groups():
    """
    Fetch all groups from the Google Workspace service with pagination.
    
    Args:
    service: The Google Workspace service object.

    Returns:
    list: A list of all groups.
    """
    service = get_service_workspace()

    groups = []
    total_groups_count = 0
    page_token = None

    try:
        while True:
            results_fetch_groups = service.groups().list(customer=customer_id, maxResults=500, pageToken=page_token).execute()
            fetched_groups = results_fetch_groups.get('groups', [])
            if not fetched_groups:
                break  # Break if no more groups are returned
            
            groups.extend(fetched_groups)
            total_groups_count += len(fetched_groups)
            page_token = results_fetch_groups.get('nextPageToken')
            if not page_token:
                break
        print(f"Total groups fetched: {total_groups_count}")

    except HttpError as error:
        print(f"An error occurred: {error}")

    return groups

def fetch_group_aliases(service, group_key):
    """
    Fetch aliases for a specific group with retry logic.

    Args:
    service: The Google Workspace service object.
    group_key: The email of the group.

    Returns:
    tuple: The group key and a list of aliases.
    """
    max_retries = 3
    for attempt in range(max_retries):
        try:
            alias_results = service.groups().aliases().list(groupKey=group_key).execute()
            return group_key, alias_results.get('aliases', [])
        except HttpError as error:
            print(f"Attempt {attempt + 1} - An error occurred while fetching aliases for group {group_key}: {error}")
            time.sleep(2 ** attempt)  # Exponential backoff
        except Exception as e:
            print(f"Attempt {attempt + 1} - A general error occurred: {e}")
            time.sleep(2 ** attempt)
    return group_key, []  # Return an empty list if all retries fail

def get_group_aliases():
    """
    Fetch all group aliases using concurrent requests.
    
    Returns:
    list: A list of group aliases with their details.
    """
    service = get_service_workspace()
    group_aliases_list = []

    # Fetch all groups
    groups = get_groups()

    print(f"Number of groups to process: {len(groups)}")

    # Process groups concurrently
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_group = {executor.submit(fetch_group_aliases, service, group['email']): group for group in groups}
        print(f'Processing group: {len(future_to_group)}')

        with tqdm(total=len(future_to_group), desc="Fetching Group Aliases") as pbar:
            for future in as_completed(future_to_group):
                try:
                    group_key, group_aliases = future.result()
                    pbar.update(1)
                    print(f"\nProcessed group: {group_key}")
                    for alias in group_aliases:
                        each_record = [
                            alias.get('alias', ''),
                            group_key,
                            "GROUP",
                            alias.get('id', ''),  # Ensure ID is included
                            alias.get('etag', '')  # Ensure ETAG is included
                        ]
                        group_aliases_list.append(each_record)
                except Exception as e:
                    print(f"An error occurred while processing group: {e}")

    print(f"All group aliases have been processed")
    return group_aliases_list

def get_group_aliases_batch():
    service = get_service_workspace()
    
    group_aliases_list = []
    total_groups_count = 0
    page_token = None

    try:
        while True:
            results_fetch_groups = service.groups().list(customer=customer_id, maxResults=500, pageToken=page_token).execute()
            groups = results_fetch_groups.get('groups', [])
            total_groups_count += len(groups)
            page_token = results_fetch_groups.get('nextPageToken')
            if not page_token:
                break
        print(f"Total groups to process: {total_groups_count}")

        with tqdm(total=total_groups_count, desc="Fetching Group Aliases") as pbar:
            for group in groups:
                pbar.update(1)
                group_key = group['email']
                alias_results = service.groups().aliases().list(groupKey=group_key).execute()
                group_aliases = alias_results.get('aliases', [])
                for alias in group_aliases:
                    each_record = [
                        alias.get('alias', ''),
                        group_key,
                        "GROUP",
                        alias.get('id', ''),  # Ensure ID is included
                        alias.get('etag', '')  # Ensure ETAG is included
                    ]
                    group_aliases_list.append(each_record)
        print(f"All group aliases have been processed")

    except HttpError as error:
        print(f"An error occurred: {error}")

    return group_aliases_list

def get_domain_list(): # GET LIST OF DOMAINS
    service = gauth.set_workspace_admin_credentials()
    domains_list = []
    total_domains_count = 0

    try:
        #fetch all domains and count them
        results_fetch_domains = service.domains().list(customer=customer_id).execute()
        domains = results_fetch_domains.get('domains', [])
        #pprint.pprint(results_fetch_domains)
        for domain in domains: #parse domains array into list and insert header row
            try:
                domainName = domain['domainName']
            except KeyError:
                domainName = ''
            try:
                verified = domain['verified']
            except KeyError:
                verified = ''
            try:
                isPrimary = domain['isPrimary']
            except KeyError:
                isPrimary = ''
            try:
                etag = domain['etag']
            except KeyError:
                etag = ''
            try:
                timestamp_str = domain['creationTime']
                #print(f"str is {timestamp_str}")
                # Convert string to datetime object in UTC timezone
                timestamp_int = int(timestamp_str)
                #print(f"int is {timestamp_int}")
                timestamp_ms = timestamp_int/1000
                #print(f"ms is {timestamp_int}")
                timestamp_dt = datetime.fromtimestamp(timestamp_ms, tz=timezone.utc)
                #print(f"dt is {timestamp_dt}")
                # Format the datetime as a more readable string
                creationTime = timestamp_dt.strftime('%Y-%m-%d %H:%M:%S')
                
            except KeyError:
                creationTime = ''

            each_domain = [
                domainName,
                verified,
                isPrimary,
                etag,
                creationTime
                ]
            domains_list.append(each_domain)
            domains_list.sort()
            total_domains_count += 1
        domains_list.insert(0,[
            'Domain Name',
            'Verified',
            'Is Primary',
            'etag',
            'Creation Time'])
        print(f"Total domains: {total_domains_count}")

        return domains_list
    except HttpError as error:
        return print(f"An error occurred: {error}")

def update_user_department(email, department):
    """Update the department for a user in Google Workspace Admin."""
    admin_service = get_service_workspace()
    
    try:
        user = admin_service.users().get(userKey=email).execute()
        orgs = user.get('organizations', [])
        
        # Check if the organization entry exists
        updated = False
        for org in orgs:
            if org.get('primary', False):
                org['department'] = department
                updated = True
                break
        
        # If no primary organization exists, create a new one
        if not updated:
            orgs.append({
                'customType': '',
                'department': department,
                'description': '',
                'primary': True,
                'title': ''
            })
        
        user['organizations'] = orgs
        updated_user = admin_service.users().update(userKey=email, body=user).execute()
        return updated_user
    
    except Exception as e:
        raise ValueError(f"Failed to update {email}: {e}")
    
def update_user_employeeType(email, employee_type):
    """Update the Employee Type for a user in Google Workspace Admin."""
    admin_service = get_service_workspace()
    
    try:
        user = admin_service.users().get(userKey=email).execute()
        orgs = user.get('organizations', [])
        
        # Check if the organization entry exists
        updated = False
        for org in orgs:
            if org.get('primary', False):
                org['description'] = employee_type
                updated = True
                break
        
        # If no primary organization exists, create a new one
        if not updated:
            orgs.append({
                'description': employee_type,
            })
        
        user['organizations'] = orgs
        updated_user = admin_service.users().update(userKey=email, body=user).execute()
        return updated_user
    
    except Exception as e:
        raise ValueError(f"Failed to update {email}: {e}")

def get_user_by_email(primary_email):
    service = get_service_workspace()
    try:
        # Retrieve user by primary email
        user = service.users().get(userKey=primary_email).execute()
        # If successful, print user details
        print(f"User found:")
        print(f"Primary Email: {user.get('primaryEmail')}")
        print(f"Name: {user.get('name', {}).get('fullName')}")
        print(f"Org Unit Path: {user.get('orgUnitPath')}")
        return user
    except HttpError as e:
        if e.resp.status == 404:
            print(f"User with primary email {primary_email} does not exist.")
        else:
            print(f"An error occurred: {e}")
        return None
    
def check_user_exists(email):
    try:
        # Execute the GAM command
        result = subprocess.run(['gam', 'info', 'user', email], capture_output=True, text=True, check=True)
        
        # Check if the result contains user details
        if 'Error: No such user' in result.stderr:
            return {'email': email, 'exists': False}
        else:
            return {'email': email, 'exists': True, 'details': result.stdout}
    
    except subprocess.CalledProcessError as e:
        # Check the error message for 'No such user' if it appears in stderr
        if 'Error: No such user' in e.stderr:
            return {'email': email, 'exists': False}
        else:
            # Handle other types of errors
            print(f"An error occurred: {e.stderr}")
            return {'email': email, 'exists': False, 'error': str(e.stderr)}

    except Exception as e:
        # Handle unexpected errors
        print(f"An unexpected error occurred: {e}")
        return {'email': email, 'exists': False, 'error': str(e)}
        
def check_employee_exists(employee_id):
    service = get_service_workspace()
    domain = 'alphamediausa.com'
    organization_value = employee_id
    
    try:
        # Initialize the list of users
        users = []
        page_token = None
        
        while True:
            # List users
            response = service.users().list(
                domain=domain,  # Replace with your domain
                maxResults=100,           # Adjust as needed
                pageToken=page_token,
                fields="users(primaryEmail,externalIds),nextPageToken"
            ).execute()

            users.extend(response.get('users', []))
            page_token = response.get('nextPageToken')

            if not page_token:
                break
        
        # Debug: Print the number of users retrieved
        print(f"Total users retrieved: {len(users)}")
        
        # Search for the user with the specified organization value
        for user in users:
            external_ids = user.get('externalIds', [])
            print(f"Checking user: {user.get('primaryEmail')}, External IDs: {external_ids}")  # Debug output
            for external_id in external_ids:
                # Strip any extra whitespace and ensure exact match
                type_match = external_id.get('type') == 'organization'
                value_match = external_id.get('value').strip() == organization_value.strip()
                
                if type_match and value_match:
                    primary_email = user.get('primaryEmail')
                    print(f"User with organization value {organization_value} found.")
                    print(f"Primary Email: {primary_email}")
                    return True, primary_email
        
        print(f"User with organization value {organization_value} does not exist.")
        return False, None

    except HttpError as e:
        print(f"An error occurred: {e}")
        return False, None

def validate_emails_in_report(report):
    results_validate = []
    failed_emails = []
    
    for entry in report:
        # Extract work email address
        work_email = entry.get('Work EMail')
        
        if work_email:
            print(f'Checking Work Email: {work_email}')
            result = check_user_exists(work_email)
            
            if result['exists']:
                results_validate.append(result)
            else:
                failed_emails.append(work_email)
    
    return results_validate, failed_emails
           
def prompt_user_for_failed_emails(failed_emails):
    if failed_emails:
        print("\nThe following email addresses were not found:")
        pprint.pprint(failed_emails)
        
        user_input = input("Do you want to process these email addresses as new accounts? (yes/no): ").strip().lower()
        
        if user_input == 'yes':
            print("Processing new accounts...")
            # Add your logic to process new accounts here
            # For example, you might want to write these emails to a file or add them to a queue
            process_new_accounts(failed_emails)
        else:
            print("No action will be taken on the failed emails.")
    else:
        print("All emails were found.")

def create_user(primary_email, first_name, last_name, password, org_unit=None, suspended=False, admin=False):
    # Construct the GAM command
    command = [
        'gam', 'create', 'user', primary_email,
        'firstname', first_name,
        'lastname', last_name,
        'password', password
    ]
    
    if org_unit:
        command.extend(['orgunit', org_unit])
    if suspended:
        command.append('suspended')
        command.append(str(suspended).lower())
    if admin:
        command.append('admin')
        command.append(str(admin).lower())
    
    # Run the command
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("User created successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("An error occurred while creating the user:")
        print(e.stderr)

            
def main():
    try:
        #print('Gathing a list...\n')
        #results = get_service_workspace()
        #results = get_users()
        #results = get_user_aliases_batch()
        #results = get_user_aliases_old()
        results = get_users_summary()
        #results = get_groups()
        #results = get_group_aliases()
        #results = get_group_aliases_batch()
        #results = get_auto_forwarding_settings()
        #results = get_domain_list()
        #results = get_domain_list()
        employee_id = 99914
        #results = check_employee_exists(employee_id)
        primary_email = 'inactive.brian.studstill@alphamediausa.com'
        #results = get_user(primary_email)
        #results = check_user_exists(primary_email)
        
        # Example usage
        #command = 'gam print aliases'
        #results = run_gam_command(command)

        #pprint.pprint(f'Results count: {len(results)}')
        pprint.pprint(results)
        
        print('successful test')
    except Exception as err:
        print(f"An error occurred getting list: {err}")

if __name__ == '__main__':
    main()

import sys
sys.path.append('g:/my drive/Python')
from _SHARED_._common_imports import *


def main():
    user_list = True
    try:
        service = gauth.set_workspace_admin_credentials()
    except Exception as err:
        print(f"An error occurred setting service credentials: {err}")
    try:
        user_list = gw.get_users(service)
    except Exception as err:
        print(f"An error occurred getting users: {err}")
    
    try:
        if user_list: user_aliases = gw.get_user_aliases(user_list, service)
    except Exception as err:
        print(f"An error occurred getting user aliases: {err}")
    
    try:
        group_aliases = gw.get_group_aliases(service)
    except Exception as err:
        print(f"An error occurred getting group aliases: {err}")

    try:
        aliases = group_aliases + user_aliases
        gs.printToSheet(aliases)
    except Exception as err:
        print(f"An error occurred exporting to google sheet: {err}")
"""

    try:
        pass #gc.sendChatMessage()
    except Exception as err:
        print(f"An error occurred sending chat group notification: {err}")
"""
if __name__ == '__main__':
    main()

# Authentication (replace with your credentials and scopes)
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'C:\\Users\\bill.mcdonald_alpham\\Documents\\Python\\Google\\service_account_key.json',
    scopes=[
        'https://www.googleapis.com/auth/admin.directory.user'
        ]
    )
http = credentials.authorize(httplib2.Http())

with open(
    'c:\\users\\bill.mcdonald_alpham\\Documents\\Python\\api_accounts.json',
    'r') as api_accounts:
    api_keys = json.load(api_accounts)
google_api_info = api_keys['google'][0]


service = build('admin', 'directory_v1', http=http)

# # Retrieve user data (adjust parameters as needed)
# results = service.users().list(customer='C02wg51jy', maxResults=500).execute()
# page = 1
# user_list = []

last_export_date = datetime.date.today().strftime("%Y-%m-%d")
count = 0

# RETRIEVE VALUES FROM LIST
google_sheet_id = '1DMlRRyVXaLI33GuNwpi4S1kKSevidfo5mn6u3-aevrE'
google_sheet_name = 'Sheet25'
google_sheet_range = f'{google_sheet_name}!$C$2:$E$5'
# google_sheet_range_date_updated = f'{google_sheet_name}!$C$1:$D$2'

users_and_pacorIDs = []
skipped_users = []

result = gsf.read_sheet(google_sheet_id, google_sheet_range, google_api_info)

currentid = ''
newid = ''

for row in result: 
    emailAddress = row[0]
    employeeId = row[2]

    users_and_pacorIDs.append({
        'email': emailAddress,
        'employeeId': employeeId
    })
    
for row in users_and_pacorIDs:
    user = row['email']  # Replace with the user's email address
    field_type = 'organization'  # Replace with the field type you want to update or create
    field_value = row['employeeId']  # Replace with the new value
    err = 'no'    
    # Retrieve existing user data
    try:
        user_info = service.users().get(userKey=user).execute()
    except HttpError:
        print(f'Can\'t find user: {user}')
        err = 'yes'
    

    # SERVICE ACCOUNT CANNOT MODIFY ANY ACCOUNTS WITH ADMIN RIGHTS
    if user_info['isAdmin'] == True:
        print(f'{user} is an Admin and cannot be modified by this service account')
        skipped_users.append({'user': user,'reason': 'isAdmin=True'})
        err = 'yes'
    # SERVICE ACCOUNT CANNOT MODIFY ANY ACCOUNTS WITH DELIGATEDADMIN RIGHTS
    if user_info['isDelegatedAdmin'] == True:
        print(f'{user} has delegatedAdmin rights and cannot be modified by this service account')
        skipped_users.append({'user': user,'reason': 'isDelegatedAdmin=True'})
        err = 'yes'

        
    if err == 'no':
        # Check if the field exists and update or create it
        external_ids = user_info.get('externalIds', [])
        # pprint.pprint(f'Current external_ids{external_ids}')
        external_id_found = None
        for external_id in external_ids:
            if external_id['type'] == field_type:
                currentid = external_id['value']
                external_id_found = external_id
                break

        if external_id_found:
            external_id_found['value'] = field_value  # Update existing field
        else:
            external_ids.append({
                'type': field_type,
                'value': field_value  # Create new field
            })
        # pprint.pprint(f'current id {currentid} new id {field_value}')
        user_info['externalIds'] = external_ids
        # pprint.pprint(user_info)
        # response = input("Do you want to continue? (y/n): ")
        # if response.lower() == 'y':
        #     print("Continuing...")
        #     # Update the user with the modified fields
        #     updated_user = service.users().update(userKey=user, body=user_info).execute()
            
        #     print(f'{user} updated successfully')
        # else:
        #     print(f"Skipping {user}")
            # Update the user with the modified fields
        updated_user = service.users().update(userKey=user, body=user_info).execute()
        
        print(f'{user} updated successfully')
pprint.pprint(skipped_users)






























# pprint.pprint(users_and_pacorIDs)
            
        # # Parse the UTC datetime string
        # utc_dateLastLogin_str = user['lastLoginTime']
        # utc_dateLastLogin = datetime.datetime.fromisoformat(utc_dateLastLogin_str)
        # # Convert to local datetime
        # dateLastLogin = utc_dateLastLogin.astimezone()  # Automatically uses your system's local time zone
        # # Print the local datetime in a readable format
        # dateLastLogin = dateLastLogin.strftime("%Y-%m-%d")  # Example output: 2024-01-25 14:00:24 PST

        # # Parse the UTC datetime string
        # utc_dateCreated_str = user['creationTime']
        # utc_dateCreated = datetime.datetime.fromisoformat(utc_dateCreated_str)
        # # Convert to local datetime
        # dateCreated = utc_dateCreated.astimezone()  # Automatically uses your system's local time zone
        # # Print the local datetime in a readable format
        # dateCreated = dateCreated.strftime("%Y-%m-%d")  # Example output: 2024-01-25 14:00:24 PST
# # User information
# user_email = 'peoriagoogleanalytics@alphamediausa.com'  # Replace with the user's email address
# custom_field_key = 'employeeID'
# new_value = '99095'  # Replace with the new value
















# # BUILD SHEET CONTENT
# resultsData = []
# date_of_export = ['Last export:', last_export_date]
# resultsData.append(date_of_export)
# total_results = ['Total Records',count]
# resultsData.append(total_results)
    
# sheetResultsData = {'values': resultsData}
# sheetContentUsers = {'values': user_list}

# cells_updated = 0

# google_sheet_id = '1DMlRRyVXaLI33GuNwpi4S1kKSevidfo5mn6u3-aevrE'
# google_sheet_name = 'python_google_users'
# google_sheet_range = f'{google_sheet_name}!$A$6:$R'
# google_sheet_range_date_updated = f'{google_sheet_name}!$C$1:$D$2'

# # CLEAR SHEET
# if gsf.clear_sheet(spreadsheetId=google_sheet_id, range=google_sheet_range, api=google_api_info):
#     print('Successfully cleared sheet')
# else:
#     print("An error occurred attempting to clear the Google Sheet")

# # CLEAR CELL
# if gsf.clear_sheet(spreadsheetId=google_sheet_id, range=google_sheet_range_date_updated, api=google_api_info):
#     print('Successfully cleared sheet')
# else:
#     print("An error occurred attempting to clear the Google Sheet")


# # # WRITE DATE TO CELL
# if gsf.append_sheet(spreadsheetId=google_sheet_id, range=google_sheet_range_date_updated, body=sheetResultsData, api=google_api_info):
#     print('Successfully wrote date to cell')
# else:
#     print("An error occurred attempting to write data to the Google Sheet cell")

# # WRITE TO USERS OT SHEET
# if gsf.append_sheet(spreadsheetId=google_sheet_id, range=google_sheet_range, body=sheetContentUsers, api=google_api_info):
#     print('Successfully wrote to sheet')
# else:
#     print("An error occurred attempting to write data to the Google Sheet")


# webhook_helpdesk_url = 'https://chat.googleapis.com/v1/spaces/AAAANM5xDUo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=d9DXKzipuuwgahqp9k7pPqen7JcIqXg4xHjHkNVDxBY'
# webhook_test_url = 'https://chat.googleapis.com/v1/spaces/AAAA9aaaByI/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=HaO9qHqrqRROfFfGQVOJbdiax5Njzd7bHLCiYU7RoQU'
# hyperlink_url = 'https://docs.google.com/spreadsheets/d/10RCr3lnkiyHQ8_8Rqgzeq-gBhVkPvVF3CAg78rQlN8E/edit#gid=505018544'
# hyperlink_text = 'Google Workspace Audit'
# message = 'Google Workspace User report has been updated'
# # chat_message.message_helpdesk(webhook_helpdesk_url,hyperlink_text,hyperlink_url,message)


import httplib2, pprint, json, datetime
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import Google.Utils.google_sheets_functions as gsf
from googleapiclient.errors import HttpError
import Google.Utils.chat_message as chat_message


# Authentication (replace with your credentials and scopes)
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user.readonly',
          'https://www.googleapis.com/auth/admin.directory.device.mobile.readonly'
          ]
SERVICE_ACCOUNT_FILE = 'Google\\service_account_key.json'  

with open(
    'api_accounts.json',
    'r') as api_accounts:
    api_keys = json.load(api_accounts)
google_api_info = api_keys['google'][0]

# Retrieve user devices 
#def get_assigned_devices():
 # try:
credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
service = build('admin', 'directory_v1', credentials=credentials)
    
#users = service.users().list(customer='C02wg51jy', maxResults=500).execute()
#devices = []
devices_result = service.mobiledevices().list(customerId='C02wg51jy', maxResults=5).execute()
pprint.pprint(devices_result)

#     for user in users['users']:
#       user_email = user['primaryEmail']
#       devices_result = service.mobiledevices().list(userKey=user_email).execute()

#       for device in devices_result.get('mobileDevices', []):
#         device_info = {
#             'user_email': user_email,
#             'device_id': device['id'],
#             'device_type': device['type'],
#             'os_version': device.get('operatingSystemVersion', 'N/A'),
#             'last_sync': device.get('lastSync', 'N/A')
#         }
#         devices.append(device_info)

#     return devices

#   except HttpError as error:
#     print(f"An error occurred: {error}")
#     return None

# pprint.pprint(get_assigned_devices())

# if __name__ == '__main__':
#   devices = get_assigned_devices()
#   if devices:
#     print("List of company-owned devices and assigned users:")
#     for device in devices:
#       print(f"User: {device['user_email']}")
#       print(f"Device ID: {device['device_id']}")
#       print(f"Device Type: {device['device_type']}")
#       print(f"OS Version: {device['os_version']}")
#       print(f"Last Sync: {device['last_sync']}")
#       print("-" * 20)
#   else:
#     print("No devices found.")

# page = 1
# user_list = []

# date_of_export = datetime.date.today().strftime("%Y-%m-%d")
# last_export_date = date_of_export
# count = 0

# while results:
#     users = results.get('users', [])
#     if page == 1:

#         user_list = []
#         headers = ['="First Name ("&COUNTA(A7:A)&")"',
#                    'Last Name',
#                    'Primary Email',
#                    'OU',
#                    'Suspended',
#                    'Last Login',
#                    'Recovery Email',
#                    'Employee ID',
#                    'Employee Type',
#                    'Employee Title',
#                    'Employee Department',
#                    'Manager Email',
#                    '2SV Enrolled',
#                    '2SV Enforced',
#                    'Admin',
#                    'Delegated Admin',
#                    'Change Password at next login',
#                    'Created'
#                    ]
#         user_list.append(headers)
    
#     # Process the current page of users
#     for user in users:
#         count +=1

#         employeeId = ''
#         for external_id in user.get('externalIds', []):
#             if "type" in external_id and external_id["type"] == "organization" and external_id["value"] != '':
#                 employeeId = external_id["value"]
#                 break  # Exit the loop once employee ID is found

#         if 'recoveryEmail' in user:  # Handle potential missing 'externalIds' list
#             recoveryEmail = user['recoveryEmail']
#         else:
#             recoveryEmail = ''
            
#         employeeTitle = ''
#         employeeDepartment = ''
#         employeeType = ''
#         for organization in user.get('organizations', []):
#             if 'title' in organization:
#                 employeeTitle = organization['title']
#             if 'department' in organization:
#                 employeeDepartment = organization['department']
#             if 'description' in organization:
#                 employeeType = organization['description']
# # print(organizationTitle)
#                 break
            
#         managerEmail = ''
#         for manager in user.get('relations', []):
#             if 'type' in manager and manager['type'] == 'manager':
#                 managerEmail = manager['value']
# # print(organizationTitle)
#                 break

            
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
            
    # # if(user['name']['familyName'] == 'Blahak' or user['name']['familyName'] == 'Freemont'):
    #     each_record = [
    #         user['name']['givenName'],
    #         user['name']['familyName'],
    #         user['primaryEmail'],
    #         user['orgUnitPath'].lstrip("/"),
    #         user['suspended'],
    #         dateLastLogin,
    #         recoveryEmail,
    #         employeeId,
    #         employeeType,
    #         employeeTitle,
    #         employeeDepartment,
    #         managerEmail,
    #         user['isEnrolledIn2Sv'],
    #         user['isEnforcedIn2Sv'],
    #         user['isAdmin'],
    #         user['isDelegatedAdmin'],
    #         user['changePasswordAtNextLogin'],
    #         dateCreated
    #     ]
    #     user_list.append(each_record)

#     # Check for next page
#     page_token = results.get('nextPageToken')
#     if page_token:
#         results = service.users().list(customer='C02wg51jy', pageToken=page_token).execute()
#         page += 1
#     else:
#         break  # No more pages
# # Process and save user data
# # pprint.pprint(results)

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
#     print('Successfully cleared cell')
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
# chat_message.message_helpdesk(webhook_helpdesk_url,hyperlink_text,hyperlink_url,message)


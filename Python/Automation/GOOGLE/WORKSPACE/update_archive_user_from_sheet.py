### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###
import _functions as fxns

success = False
title = "Google Archive User"
content = "Google Archive User completed successfully."
targetGroup = 2
worksheetIndex = 1
sheetIndex = 99
path = get_caller_file_and_folder_names()
    
def task(email):
    return fxns.run_gam_command(f'gam update user {email} archived true')

def get_users_to_archive_list():
    try:
        print("Collecting data list...")
        sheet_data = gs.read_sheet(worksheetIndex, sheetIndex)
        return sheet_data
    except Exception as err:
        print(f"An error occurred getting users: {err}")
        return


def main(sendMsg=False):
    try:
        sheet_data = get_users_to_archive_list()
        for row in sheet_data:
            email = row[0]  # Assuming the email is in the first column of each row
            try:
                results, execution_time = task_execution_time(lambda: task(email))
                #pprint.pprint(results)
                success = True  # Adjust based on your success criteria
            except Exception as err:
                print(f"An error occurred running gam command for {email}: {err}")

        if success and sendMsg:
            gc.sendChatMessage(title, content, targetGroup)
        elif not sendMsg:
            print("Message sending disabled")
    except Exception as err:
        print(f"An error occurred during the main process: {err}")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run script with optional message sending.")
    parser.add_argument('--sendMsg', action='store_true', help='Send message when true')
    args = parser.parse_args()

    main(sendMsg=args.sendMsg)
### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###
import _functions as fxns

success = False
title = "ZenDesk Suspended Users Ticket Counts Export"
content = "ZenDesk Suspended Users Ticket Counts Export has completed successfully."
targetChat = 2
worksheetIndex = 1
sheetIndex = 73
path = get_caller_file_and_folder_names()

def task():
    all_users = fxns.get_all_end_users()
    suspended_users = fxns.filter_suspended_users(all_users)
    return fxns.get_users_with_ticket_counts(suspended_users)

def main(sendMsg=False):
    try:
        print("Getting ZenDesk End-Users...")
        results, execution_time = task_execution_time(task, print=False)
    except Exception as err:
        print(f"An error occurred getting end-users: {err}")
        return

    try: # EXPORT TO GOOGLE SHEET
        data = results
        gs.printToSheet(execution_time, path, data, worksheetIndex, sheetIndex)
        success = True
                
    except Exception as err:
        print(f"An error occurred exporting to google sheet: {err}")

    try:
        if success and sendMsg:
            gc.sendChatMessage(title, content, targetChat)
        if sendMsg==False:
            print("Message sending disabled")
    except Exception as err:
        print(f"An error occurred sending chat group notification: {err}")

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run script with optional message sending.")
    parser.add_argument('--sendMsg', action='store_true', help='Send message when true')
    args = parser.parse_args()

    main(sendMsg=args.sendMsg)
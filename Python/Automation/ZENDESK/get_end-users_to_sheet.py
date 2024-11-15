### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###
import _functions as fxns

success = False
title = "ZenDesk End-Users Export"
content = "ZenDesk End-Users Export has completed successfully."
path = get_caller_file_and_folder_names()
targetChat = 2
worksheetIndex = 1
sheetIndex = 71
path = get_caller_file_and_folder_names()

def task():
    return fxns.get_all_end_users()

def main(sendMsg=False):
    try:
        print("Getting ZenDesk End-Users...")
        results, execution_time = task_execution_time(task, print=False)
                
    except Exception as err:
        print(f"An error occurred getting end-users: {err}")
        return

    try:
        print("Converting records for sheets injection...")
        data = fxns.format_for_google_sheets(results)
        pprint.pprint(data[:2])
        
    except Exception as err:
        print(f"An error occurred getting results: {err}")
        return

    try: # EXPORT TO GOOGLE SHEET
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
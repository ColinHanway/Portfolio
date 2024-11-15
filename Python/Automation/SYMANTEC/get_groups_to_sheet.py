### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###

success = False
title = "Symantec Groups Export"
content = "Symantec Groups Export has completed successfully."
worksheetIndex = 1
sheetIndex = 22
targetGroup = 2
path = get_caller_file_and_folder_names()

def task():
    return sym.fetch_groups_list()

def main(sendMsg=False):
    try:
        print("Collecting Symantec Groups list...")
        results, execution_time = task_execution_time(task, print=False)
    except Exception as err:
        print(f"An error occurred running gam command: {err}")

    # Print to sheet
    try: # EXPORT TO GOOGLE SHEET
        data = results
        gs.printToSheet(execution_time, path, data, worksheetIndex, sheetIndex)
        success = True
    except Exception as err:
        print(f"An error occurred exporting to google sheet: {err}")

    # Send confirmation message
    try:
        if success and sendMsg:
            gc.sendChatMessage(title, content, targetGroup)
        if sendMsg==False:
            print("Message sending disabled")
    except Exception as err:
        print(f"An error occurred sending chat group notification: {err}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run script with optional message sending.")
    parser.add_argument('--sendMsg', action='store_true', help='Send message when true')
    args = parser.parse_args()

    main(sendMsg=args.sendMsg)
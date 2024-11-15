### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###
import _functions as fxns

success = False
title = "Google Aliases Export"
content = "Google Aliases Export has completed successfully."
targetGroup = 2
worksheetIndex = 1
sheetIndex = 2
path = get_caller_file_and_folder_names()
    
def task():
    return fxns.run_gam_command('gam print aliases')

def main(sendMsg=False):
    try:
        results, execution_time = task_execution_time(task, print=False)
    except Exception as err:
        print(f"An error occurred running gam command: {err}")

    try: # EXPORT TO GOOGLE SHEET
        print(f"Converting CSV to LIST")
        data = parse_csv_to_list(results)
        success = True
    except Exception as err:
        print(f"An error occurred exporting to google sheet: {err}")

    try: # EXPORT TO GOOGLE SHEET
        print(f"Sending aliases to sheet: {len(data)}")
        gs.printToSheet(execution_time, path, data, worksheetIndex, sheetIndex)
        success = True
    except Exception as err:
        print(f"An error occurred exporting to google sheet: {err}")

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
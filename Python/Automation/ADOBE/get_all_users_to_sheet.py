### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###
import _functions as fxns


def main(sendMsg=False):
    success = False
    title = "Adobe Users Export"
    content = "Adobe Users Export has completed successfully."
    path = get_caller_file_and_folder_names()
    targetChat = 2
    worksheetIndex = 1
    sheetIndex = 41

    try:
        data = fxns.get_all_users()
        pprint.pprint(data[:2])
        save_data_to_file(data, title)
    except Exception as err:
        print(f"An error occurred getting users: {err}")
        return

    try:
        formatted_data = format_responses_for_sheets(data)  
        pprint.pprint(formatted_data[:2])
    except Exception as err:
        print(f"An error occurred formatting for Sheets: {err}")
        return
    
    try: # EXPORT TO GOOGLE SHEET
        gs.printToSheet(path, formatted_data, worksheetIndex, sheetIndex)
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
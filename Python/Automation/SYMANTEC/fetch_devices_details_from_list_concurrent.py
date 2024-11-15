### GLOBAL IMPORTS ###
#
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *
#
#####################

### LOCAL IMPORTS ###
#

#
#####################

success = False
title = "Symantec Device Details Export"
content = "Symantec Device Details Export has completed successfully."
path = get_caller_file_and_folder_names()
targetGroup = 2
worksheetIndex = 1
sheetIndex = 7

# Main execution
def main(sendMsg=False):
    
    access_token = sym.get_access_token()
    
    if access_token:
        print("Collecting Symantec Device details...")
        start_time = time.time()  # Start the timer
        device_details_list = sym.fetch_devices_details_from_list_concurrent()
        end_time = time.time()  # End the timer
        execution_time = round(end_time - start_time, 2)  # Calculate the execution time
    else:
        print('Unable to fetch device information.')

# Print to sheet
    try: # EXPORT TO GOOGLE SHEET
        data = device_details_list
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
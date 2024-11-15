### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###
import GOOGLE.WORKSPACE._functions as gw
import _functions as fxns

success = False
title = "Google Vault Open Matters Details Export"
content = "Google Vault Open Matters Details Export has completed successfully."
targetGroup = 2
worksheetIndex = 1
sheetIndex = 9
path = get_caller_file_and_folder_names()
total_execution_time = 0
  
def get_vault_matters():
    return gw.run_gam_command(f'gam print vaultmatters basic')

def get_vault_matter_details(matter_id):
    return gw.run_gam_command(f'gam print vaultholds matter id:{matter_id}')

def main(sendMsg=False):
    try:
        results, execution_time = task_execution_time(get_vault_matters)
        total_execution_time = execution_time
        #pprint.pprint(results)
        success = True
    except Exception as err:
        print(f"An error occurred running gam command: {err}")
    try:
        if success:
            open_matters_list = fxns.parse_open_matter_ids(results)
            #pprint.pprint(open_matters_list[:1])
            success = True
    except Exception as err:
        print(f"An error occurred running gam command: {err}")

    try:
        if success:
            matter_holds_list = []
            first_iteration = True
            open_matters_list = open_matters_list[1:2]
            for matter_id in open_matters_list:
                matter_details,execution_time = task_execution_time(lambda: get_vault_matter_details(matter_id))
                total_execution_time += execution_time
                try: # CONVERT CSV TO LIST
                    print(f"Converting CSV results to LIST")
                    unprocessed_rows = parse_csv_to_list(matter_details)
                    pprint.pprint(unprocessed_rows)
                    success = False
                except Exception as err:
                    print(f"An error occurred exporting to google sheet: {err}")
                processed_rows = fxns.process_matter_details(unprocessed_rows)
                pprint.pprint(processed_rows)
                return
                    
                # Include the header in the first iteration, skip it in subsequent iterations
                if first_iteration:
                    matter_holds_list.extend(rows)  # Add all rows, including the header
                    first_iteration = False  # Update the flag after the first iteration
                    print(f"Putting first iteration and headers in Holds List")
                else:
                    matter_holds_list.extend(rows[1:])  # Skip the header row in subsequent iterations
                    print(f"Adding subsequent iteration to Holds List")

            #print(f"Printing entire list... \n{matter_holds_list}")        
        success = False
    except Exception as err:
        print(f"An error occurred running gam command: {err}")

    try: # EXPORT TO GOOGLE SHEET
        if success:
            data = matter_holds_list
            print(f"Sending data to sheet: {len(data)}")
            gs.printToSheet(total_execution_time, path, data, worksheetIndex, sheetIndex)
            #success = True
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
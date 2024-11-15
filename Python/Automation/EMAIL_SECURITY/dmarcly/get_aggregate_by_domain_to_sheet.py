### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###
import _functions as fxns

success = False
title = "DMarcly Aggregate_by_domain Export"
content = "DMarcly Aggregate_by_domain Export has completed successfully."
targetGroup = 2
worksheetIndex = 3
sheetIndex = 11
path = get_caller_file_and_folder_names()
num_days=30

def task():
    return fxns.get_aggregate_by_domain(num_days)

def main(sendMsg=False):
    try:
        print(f"Collecting Dmarcly Domain summaries for {num_days}...")
        results, execution_time = task_execution_time(task, print=False)
    except Exception as err:
        print(f"An error occurred running gam command: {err}")

    try: # EXPORT TO GOOGLE SHEET
        data = results
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

def get_user_input():
    try:
        user_input_num_days = input("Getting Dmarcly Aggregate report for how many days (default=30)?")
        # Check if the user input is empty
        if user_input_num_days.strip() == "":
            print("Using default=30")
            num_days = 30
        else:
            try:
                # Convert user input to integer
                num_days = int(user_input_num_days)
            except ValueError:
                print("Invalid input. Defaulting to 30 days.")
                num_days = 30
    except Exception as err:
        print(f"An error occurred getting Dmarcly aggregate by domain list: {err}")
        return 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run script with optional message sending.")
    parser.add_argument('--sendMsg', action='store_true', help='Send message when true')
    args = parser.parse_args()

    main(sendMsg=args.sendMsg)
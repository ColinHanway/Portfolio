### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###
import _functions as fxns

success = False
title = "Cloudflare All Domains All Records Export"
content = "Cloudflare All Domains All Records Export has completed successfully"
targetChat = 2
worksheetIndex = 3
sheetIndex = 22
path = get_caller_file_and_folder_names()
total_execution_time = 0

def task():
    return fxns.get_domains_from_sheet()

def main(sendMsg=False):
    try:
        print("Collecting Cloudflare Domain IDs list...")
        results, execution_time = task_execution_time(task, print=False)
        total_execution_time = execution_time
    except Exception as err:
        print(f"An error occurred getting domain IDs: {err}")
        return

    # Format the zones data into rows
    header = [
        'Zone Name',
        'Zone ID',
        'Record Name', 
        'Record ID',
        'Record Type', 
        'Content', 
        'TTL', 
        'Proxiable',
        'Proxied',
        'Created On',
        'Modified On',
        'Comment'
    ]

    all_records = [header]
    num_domains = len(results)
    try:
        for zone_id in tqdm(results, desc=f"Fetching DNS records for all {num_domains} domains..."):
            def task2():
                return fxns.get_dns_records(zone_id)

            records, execution_time = task_execution_time(task2, print=False)
            total_execution_time += execution_time
            
            def task3():
                return fxns.transform_dns_records_for_sheets(records)
           
            formatted_records, execution_time = task_execution_time(task3, print=False)
            total_execution_time += execution_time

            all_records.extend(formatted_records)
        
    except Exception as err:
        print(f"An error occurred getting domain records: {err}")
        return []    
    
    print(f"Execution time: {total_execution_time:.2f} seconds")

    try: # EXPORT TO GOOGLE SHEET
        data = all_records
        gs.printToSheet(total_execution_time, path, data, worksheetIndex, sheetIndex)
        success = True
                
    except Exception as err:
        print(f"An error occurred exporting to google sheet: {err}")
    try:
        #sendMsg=True
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
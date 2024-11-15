### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###
import _functions as fxns

success = False
title = "Cloudflare Domain List Export"
content = "Cloudflare Domain List Export has completed successfully."
targetGroup = 2
worksheetIndex = 3
sheetIndex = 98
path = get_caller_file_and_folder_names()

def task():
    return fxns.get_all_zones()

def main(sendMsg=False):
    try:
        print("Getting all registered domains...")
        results, execution_time = task_execution_time(task, print=False)
    except Exception as err:
        print(f"An error occurred getting domains: {err}")
        return

    try:
        header = [
            'Zone Name', 
            'Zone ID', 
            'Account ID', 
            'Account Name', 
            'Activated On', 
            'Created On',
            'Development Mode', 
            'Custom Certificate Quota',
            'Page Rule Quota', 
            'Phishing Detected', 
            'Step',
            'Modified On', 
            'Name Servers',
            'Original DNS Host', 
            'Original Name Servers',
            'Original Registrar', 
            'Owner Email', 
            'Owner ID',
            'Owner Type', 
            'Paused', 
            'Permissions',
            'Plan ID', 
            'Plan Name', 
            'Plan Price', 
            'Plan Currency',
            'Plan Subscribed', 
            'Status', 
            'Tenant ID', 
            'Tenant Name',
            'Tenant Unit ID', 
            'Zone Type'
        ]
        results.insert(0,header)
    except Exception as err:
        print(f"An error occurred: {err}")
        return
        
    """
    try:
        print("Converting records for sheets injection...")
        data = cf.transform_dns_records_for_sheets(results)
        
    except Exception as err:
        print(f"An error occurred converting records: {err}")
        return
    """
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

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run script with optional message sending.")
    parser.add_argument('--sendMsg', action='store_true', help='Send message when true')
    args = parser.parse_args()

    main(sendMsg=args.sendMsg)
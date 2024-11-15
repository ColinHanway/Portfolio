### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###
import _functions as fxns


def main(sendMsg=False):
    success = False
    title = "Cloudflare Domain DNS Export"
    content = "Cloudflare Domain DNS Export has completed successfully."
    targetChat = 2
    worksheetIndex = 3
    sheetIndex = 21

    try:
        print("Getting zone ID from domain name...")
        zone_id = fxns.get_zone_id('1009theeagle.com')
        pprint.pprint(zone_id)
        
    except Exception as err:
        print(f"An error occurred getting zone ID: {err}")
        return

    try:
        print("Getting records for zone ID...")
        records = fxns.get_dns_records(zone_id)
        pprint.pprint(records)
        
    except Exception as err:
        print(f"An error occurred getting records: {err}")
        return
    
    try:
        print("Converting records for sheets injection...")
        data = fxns.transform_dns_records_for_sheets(records)
        
    except Exception as err:
        print(f"An error occurred getting records: {err}")
        return

    try: # EXPORT TO GOOGLE SHEET
        gs.printToSheet(title, data, worksheetIndex, sheetIndex)
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
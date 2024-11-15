### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###
import _functions as fxns

success = False
title = "D-Link Nuclias Device Export"
content = "D-Link Nuclias Export has completed successfully."
targetGroup = 2
worksheetIndex = 1
sheetIndex = 51

def print_to_sheet(deviceList):
    try: # EXPORT TO GOOGLE SHEET
        data = deviceList
        #pprint.pprint(data[:3])
        gs.printToSheet(title, data, worksheetIndex, sheetIndex)
        success = True
        return success
    except Exception as err:
        print(f"An error occurred exporting to google sheet: {err}")

def send_message(success,sendMsg):
    try:
        if success and sendMsg:
            gc.sendChatMessage(title, content, targetGroup)
        if sendMsg==False:
            print("Message sending disabled")
    except Exception as err:
        print(f"An error occurred sending chat group notification: {err}")
        
# Main execution
def main(sendMsg=False):
    print("Collecting D-Link Nuclias Devices list...")
    deviceList = fxns.get_devices()
    #pprint.pprint(deviceList[:3])
    success = print_to_sheet(deviceList)
    print(f"Success: {success}\nSendMsg: {sendMsg}")
    if sendMsg: send_message(success,sendMsg)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run script with optional message sending.")
    parser.add_argument('--sendMsg', action='store_true', help='Send message when true')
    args = parser.parse_args()

    main(sendMsg=args.sendMsg)
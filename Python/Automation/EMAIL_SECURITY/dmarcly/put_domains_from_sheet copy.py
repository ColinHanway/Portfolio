### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###
import _functions as fxns
    
def main(sendMsg=False):
    success = False
    title = "DMarcly Add Domains from Sheet"
    content = "DMarcly Add Domains from Sheet has completed successfully."
    targetGroup = 2

    try: # READ DOMAINS FROM GOOGLE SHEET
        results = []
        worksheetIndex = 3
        sheetIndex = 99
        results = gs.read_sheet(worksheetIndex, sheetIndex)
        success = True
    except Exception as err:
        print(f"An error occurred reading from google sheet: {err}")
        success = False
    if results:
        try: # PROCESS AND ADD DOMAINS FROM SHEET
            fxns.process_domains(results)      
        except Exception as err:
            print(f"An error occurred sending chat group notification: {err}")
            success = False
            return
        
    try: # SEND STATUS UPDATE MESSAGE 
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
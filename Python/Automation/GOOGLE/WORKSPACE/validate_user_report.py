### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###
import PAYCOR._functions as pc
import _functions as fxns

def main(sendMsg=False):
    results_report = pc.fetch_new_hire_and_termination_report()
    #pprint.pprint(results_report)
    results_validate, failed_emails = fxns.validate_emails_in_report(results_report)
    fxns.prompt_user_for_failed_emails(failed_emails)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run script with optional message sending.")
    parser.add_argument('--sendMsg', action='store_true', help='Send message when true')
    args = parser.parse_args()

    main(sendMsg=args.sendMsg)
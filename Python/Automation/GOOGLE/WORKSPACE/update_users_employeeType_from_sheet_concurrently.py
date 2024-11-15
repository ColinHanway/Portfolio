### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###
import _functions as fxns
import concurrent.futures

worksheetIndex = 1
sheetIndex = 99

def update_user(email, employee_type):
    try:
        updated_user = gw.update_user_employeeType(email, employee_type)
        return f"Updated {email} with Employee Type {employee_type}"
    except Exception as e:
        return f"Failed to update {email}: {e}"

def main():
    try:
        print("Collecting data list...")
        sheet_data = gs.read_sheet(worksheetIndex, sheetIndex)
    except Exception as err:
        print(f"An error occurred getting users: {err}")
        return
    
    # Create a list to hold future results
    results = []

    # Use ThreadPoolExecutor to run the updates concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Wrap futures with tqdm to show progress
        for future in tqdm(
            concurrent.futures.as_completed(
                {executor.submit(update_user, email, employee_type): (email, employee_type) for email, employee_type in sheet_data}
            ),
            total=len(sheet_data),
            desc="Updating users"
        ):
            try:
                result = future.result()
                print(result)
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
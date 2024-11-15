"""
First attempt parser for xlsx files
in order to sort out duplicates and save them to a new list.
"""

import os
import pandas as pd

file = "C:/Users/hanwa/Downloads/New Hire and Termination Report.xlsx"

new_workbook = pd.read_excel(file)
try:
    old_workbook = pd.read_excel("parsed_emails.xlsx", sheet_name="Seen Emails")
except ValueError:
    old_workbook = pd.DataFrame()
    old_workbook["Work EMail"] = [""]
    old_workbook["Status"] = [""]

new_workbook = new_workbook[["Status", "Work EMail"]].dropna()
old_workbook = old_workbook[["Status", "Work EMail"]].dropna()

new_status = new_workbook.set_index("Work EMail")["Status"].to_dict()
old_status = old_workbook.set_index("Work EMail")["Status"].to_dict()

rsltin_df = new_workbook[~new_workbook["Work EMail"].isin(old_workbook["Work EMail"])]

print(rsltin_df)


duplicate_emails_df = (
    pd.concat([rsltin_df, old_workbook]).reset_index(drop=True).dropna()
)

# print(newEmailsFilter)

with pd.ExcelWriter("Parsed_Emails.xlsx") as writer:
    rsltin_df.to_excel(
        writer, sheet_name="Parsed", columns=["Status", "Work EMail"], index=False
    )

    duplicate_emails_df.to_excel(
        writer, sheet_name="Seen Emails", columns=["Status", "Work EMail"], index=False
    )


delete = input("Do you want to delete the New Hire and Term report? (Y / N)")
if delete in ["y", "Y"]:
    os.remove(file)

print("Done!")

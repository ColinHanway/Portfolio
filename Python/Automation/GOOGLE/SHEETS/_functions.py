### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###
from GOOGLE.SHEETS import _sheets_index as si
from EMAIL_SECURITY.dmarcly import _functions as dmarcly 

### CLEAR SHEET ###
def clear_sheet(spreadsheet_id, range_name):
    # Get authorization for connecting to the spreadsheet
    try:
        service = gauth.set_google_sheets_credentials()
    except Exception as err:
        print(f"An error occurred setting service credentials: {err}")

    # Clear the specified range in the spreadsheet using the Google Sheets API
    try:
        body = {}  # Empty body to clear the contents
        request = service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            body=body
        )
        request.execute()
        return True  # Operation successful
    except Exception as e:
        print(f"Error clearing sheet: {e}")
        return False  # Operation failed
    
    
    
    ### WRITE TO SHEET ###

def cell_to_row_col(cell):
    """Convert cell reference to 0-based row and column indices."""
    match = re.match(r"([A-Z]+)(\d+)", cell)
    if match:
        col_letter, row_number = match.groups()
        col_index = 0
        for char in col_letter:
            col_index = col_index * 26 + (ord(char) - ord('A'))
        return int(row_number) - 1, col_index
    raise ValueError(f"Invalid cell reference: {cell}")

def parse_range(range_str):
    """Extract start and end cell references from the range string."""
    range_parts = range_str.split('!')
    sheet_name = range_parts[0].strip()
    cells = range_parts[1].strip().split(':')
    start_cell = cells[0].strip('$')
    end_cell = cells[1].strip('$') if len(cells) > 1 else start_cell
    return sheet_name, start_cell, end_cell

def append_sheet(spreadsheetId, range, body, filter=False, trim=False):
    # Get authorization for connecting to the spreadsheet
    try:
        service = gauth.set_google_sheets_credentials()
    except Exception as err:
        print(f"An error occurred setting service credentials: {err}")
        return False

    try:
        # Append the data to the sheet
        request = service.spreadsheets().values().append(
            spreadsheetId=spreadsheetId, 
            range=range, 
            body=body, 
            valueInputOption='USER_ENTERED'
        )
        response = request.execute()
        """
        if filter or trim:
            try:
                # Parse the range to get start and end rows and columns
                sheet_name, start_cell, end_cell = parse_range(range)
                sheet_id = get_sheet_id(service, spreadsheetId, sheet_name)
                start_row, start_col = cell_to_row_col(start_cell)
                start_row_index = start_row
                end_row_index = start_row + response['updates']['updatedRows']
                
                if end_cell.isalpha():
                    end_cell += str(end_row_index)
                end_row, end_col = cell_to_row_col(end_cell)
                
                end_col_index = end_col + 1

                if filter:
                    # Create a filter request
                    filter_request = {
                        "setBasicFilter": {
                            "filter": {
                                "range": {
                                    "sheetId": sheet_id,
                                    "startRowIndex": start_row_index,
                                    "endRowIndex": end_row_index,
                                    "startColumnIndex": start_col,
                                    "endColumnIndex": end_col_index
                                }
                            }
                        }
                    }
                    service.spreadsheets().batchUpdate(
                        spreadsheetId=spreadsheetId, 
                        body={"requests": [filter_request]}
                    ).execute()

                if trim:
                    # Get the current sheet dimensions
                    sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheetId, ranges=[sheet_name], fields="sheets(data(rowData, startRow, startColumn))").execute()
                    total_rows = len(sheet_metadata['sheets'][0]['data'][0]['rowData'])
                    total_cols = max(len(row['values']) for row in sheet_metadata['sheets'][0]['data'][0]['rowData'] if 'values' in row)

                    # Calculate the number of rows and columns to delete
                    rows_to_delete = total_rows - end_row_index
                    cols_to_delete = total_cols - end_col_index

                    trim_requests = []
                    if rows_to_delete > 0:
                        trim_requests.append({
                            "deleteDimension": {
                                "range": {
                                    "sheetId": sheet_id,
                                    "dimension": "ROWS",
                                    "startIndex": end_row_index,
                                    "endIndex": total_rows
                                }
                            }
                        })

                    if cols_to_delete > 0:
                        trim_requests.append({
                            "deleteDimension": {
                                "range": {
                                    "sheetId": sheet_id,
                                    "dimension": "COLUMNS",
                                    "startIndex": end_col_index,
                                    "endIndex": total_cols
                                }
                            }
                        })

                    if trim_requests:
                        service.spreadsheets().batchUpdate(
                            spreadsheetId=spreadsheetId, 
                            body={"requests": trim_requests}
                        ).execute()
            except Exception as e:
                print(f"Error during filter or trim operation: {e}")
                return False  # Operation failed    
        """

        return True  # Operation successful
    except Exception as e:
        print(f"Error writing to sheet: {e}")
        return False  # Operation failed    
        
### READ SHEET ###
def read_sheet(worksheetIndex,sheetIndex):
    try:
        service = gauth.set_google_sheets_credentials()
    except Exception as err:
        print(f"An error occurred setting service credentials: {err}")

    google_sheet_id = si.sheet_options[worksheetIndex]['id']
    google_sheet_name = si.sheet_options[worksheetIndex]['sheets'][sheetIndex]['name']
    cells_data = si.sheet_options[worksheetIndex]['sheets'][sheetIndex]['data_range']
    range_data = google_sheet_name + "!" + cells_data

    try:
        # Get the values from the sheet
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=google_sheet_id, range=range_data).execute()
        values = result.get('values', [])

        # Convert values to an array of lists
        data_array = []
        if values:
            for row in values:
                data_array.append(row)  # Append each row as a list
        return data_array  # Operation successful

    except Exception as e:
        print(f"Error reading from sheet: {e}")
        return False  # Operation failed    

### PRINT TO SHEET ###
def printToSheet(execution_time, path, data,worksheetIndex,sheetIndex):

    # BUILD DATE UPDATED, COUNT
    results = []
    
    # GET NOW DATE
    last_export_date = datetime.today().strftime("%Y-%m-%d")
    date_of_export = ['Last export', last_export_date]
    results.append(date_of_export)
    
    # COUNT RESULTS
    countData = len(data)-1
    total_results = ['Count',countData]
    results.append(total_results)


    google_sheet_id = si.sheet_options[worksheetIndex]['id']
    google_sheet_name = si.sheet_options[worksheetIndex]['sheets'][sheetIndex]['name']
    google_sheet_title = si.sheet_options[worksheetIndex]['sheets'][sheetIndex]['title']
    cells_title = si.sheet_options[worksheetIndex]['sheets'][sheetIndex]['title_range']
    cells_results = si.sheet_options[worksheetIndex]['sheets'][sheetIndex]['date_updated_range']
    cells_data = si.sheet_options[worksheetIndex]['sheets'][sheetIndex]['data_range']
    range_title = google_sheet_name + "!" + cells_title
    range_results = google_sheet_name + "!" + cells_results
    range_data = google_sheet_name + "!" + cells_data
    
    title_data = []
    title_data.append(['Title',google_sheet_title])
    title_data.append(['Script Path',path])
    title_data.append(['Execution Time (sec)',execution_time])
    sheetTitle = {'values': title_data}
    sheetDateUpdated = {'values': results}
    sheetContent = {'values': list(data)}
    #print(sheetTitle)
    #print(sheetDateUpdated)
    #return

    #pprint.pprint(sheetTitle)
    #print(f'Google Sheet ID: {google_sheet_id}\n')
    #print(f'Range results: {range_results}\n')
    #print(f'Range data: {range_data}\n')

    # CLEAR TITLE
    if clear_sheet(google_sheet_id, range_title):
        pass #print('Successfully cleared title cell')
    else:
        print("An error occurred attempting to clear the Google Sheet title range")
        return False

    # WRITE TITLE TO CELL
    if append_sheet(spreadsheetId=google_sheet_id, range=range_title, body=sheetTitle):
        pass #print('Successfully wrote title to cell')
    
    else:
        print("An error occurred attempting to write title data to the Google Sheet cell")
        return False

    # CLEAR DATE UPDATED
    if clear_sheet(google_sheet_id, range_results):
        pass #print('Successfully cleared cell')
    else:
        print("An error occurred attempting to clear the Google Sheet results range")
        return False

    # WRITE DATE UPDATED TO CELL
    if append_sheet(spreadsheetId=google_sheet_id, range=range_results, body=sheetDateUpdated):
        pass #print('Successfully wrote date to cell')
    else:
        print("An error occurred attempting to write date-updated data to the Google Sheet cell")
        return False

    # CLEAR CONTENT
    if clear_sheet(google_sheet_id, range_data):
        pass #print('Successfully cleared sheet')
    else:
        print("An error occurred attempting to clear the Google Sheet data range")
        return False

    # WRITE CONTENT TO SHEET
    if append_sheet(spreadsheetId=google_sheet_id, range=range_data, body=sheetContent, filter=True, trim=True):
        print(f'Successfully wrote content data to sheet')
    else:
        print("An error occurred attempting to write content data to the Google Sheet")
        return False
        
    return True

def main():

    try:
        path = get_caller_file_and_folder_names()
        test_data = [[1,2,3],['a','b','c']]
        test_spreadsheet_index = 1
        test_range_name = 99
        #result = printToSheet(path, test_data,test_spreadsheet_index,test_range_name)
        #result = clear_sheet(test_spreadsheet_index, test_range_name)
        result = read_sheet(test_spreadsheet_index,test_range_name)        
        print(result[:3])
        #add_domains_result = dmarcly.process_domains(data_array)
    except Exception as err:
        print(f"An error occurred testing: {err}")

if __name__ == '__main__':
    main()

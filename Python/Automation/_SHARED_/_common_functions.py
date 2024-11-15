import json,os,inspect, re, csv, io, time
import pprint
from datetime import datetime, timedelta


def get_credentials(service_name):
    keyfile_path = '_SHARED_\\api_accounts.json'
   
    try:
        with open(keyfile_path, 'r') as file:
            credentials = json.load(file)
        return credentials[service_name][0]['api_key']
    
    except Exception as e:
        print(f"An error occurred retrieving credentials: {e}")
        return None    
    
def transform_dns_records_for_sheets(records):
   
    # Create a list to hold the data rows
    data_rows = []
    
    # Transform each DNS record into a row
    for record in records:
        row = [
            record.get('zone_name'),
            record.get('zone_id'),
            record.get('name'),
            record.get('id'),
            record.get('type'),
            record.get('content'),
            record.get('ttl'),
            record.get('proxiable'),
            record.get('proxied'),
            format_date(record.get('created_on')),  # Convert to yyyy-mm-dd
            format_date(record.get('modified_on')), # Convert to yyyy-mm-dd
            record.get('comment')
        ]
        data_rows.append(row)
    
    return data_rows
    
def format_responses_for_sheets(responses):
    if not responses:
        return []

    # Extract headers from the first dictionary
    headers = list(responses[0].keys())
    
    # Prepare formatted data
    formatted_data = [headers]
    
    for response in responses:
        values = []
        for key in headers:
            value = response.get(key, "")
            if isinstance(value, list):
                value = ', '.join(map(str, value))  # Convert list to comma-separated string
            values.append(value)
        formatted_data.append(values)
    
    return formatted_data

def format_date(date_string):
    """
    Convert an ISO 8601 date string to yyyy-mm-dd format.
    
    :param date_string: The ISO 8601 date string.
    :return: A string in yyyy-mm-dd format.
    """
    if date_string:
        # Strip the trailing 'Z' and parse the datetime
        dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d')
    return None

def format_timestamp(timestamp, with_time=False):
    
    if timestamp is None:
        return None
    if with_time:
        return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')

def to_camel_case(text):
    """Convert a text to camel case."""
    # Remove spaces and split into words
    words = re.sub(r'[^a-zA-Z0-9]', ' ', text).split()
    
    # Convert first word to lowercase and the rest to title case
    return words[0].lower() + ''.join(word.capitalize() for word in words[1:])

def parse_csv_to_list(csv_data):
    # Use StringIO to treat the string as file-like object
    csv_file = io.StringIO(csv_data)
    reader = csv.reader(csv_file)

    # Initialize list to store parsed data
    data_list = []

    # Iterate over rows in the CSV
    for row in reader:
        # Append each row to the data_list
        data_list.append(row)

    return data_list

def save_data_to_file(data, title, expiration_seconds=86400):
    """Save data to a JSON file with an expiration timestamp."""
    filename = f"{title}.json"
    
    # Current timestamp and expiration time
    current_time = datetime.now().isoformat()
    expiration_time = (datetime.now() + timedelta(seconds=expiration_seconds)).isoformat()
    
    data_with_expiration = {
        "timestamp": current_time,
        "expiration": expiration_time,
        "data": data
    }
    
    try:
        with open(filename, 'w') as file:
            json.dump(data_with_expiration, file, indent=4)
        print(f"Data successfully saved to {filename}")
    except IOError as e:
        print(f"An error occurred writing the file: {e}")
        
def get_caller_file_and_folder_names():
    # Get the caller's frame
    frame = inspect.currentframe().f_back
    
    # Get the caller's file name and directory
    caller_file = frame.f_code.co_filename
    caller_folder = os.path.basename(os.path.dirname(caller_file))
    
    # Extract the file name from the file path
    file_name = os.path.basename(caller_file)
    
    # Combine them into a single text string
    result = f"{caller_folder}\\{file_name}"
    
    return result

def get_all_keys_from_list_of_dicts(devices_list):
    all_keys = set()  # Using a set to avoid duplicate keys
    for device in devices_list:
        if isinstance(device, dict):  # Ensure the device is a dictionary
            all_keys.update(device.keys())  # Add keys from each dictionary
    return list(all_keys)  # Convert set back to list for further use

def convert_to_list_of_lists(devices_list, keys):
    list_of_lists = [keys]  # Include headers as the first row
    for device in devices_list:
        if isinstance(device, dict):  # Ensure device is a dictionary
            row = [device.get(key, 'N/A') for key in keys]  # Extract values by key, default to 'N/A' if missing
            list_of_lists.append(row)
    return list_of_lists

# not working. Not sure I can pass a function here
def task_execution_time(task,should_print=True):
    start_time = time.time()  # Start the timer
    results = task()
    end_time = time.time()  # End the timer
    execution_time = round(end_time - start_time, 2)  # Calculate the execution time
    if should_print==True:
        print(f"Execution time: {execution_time:.2f} seconds")
    return results, execution_time
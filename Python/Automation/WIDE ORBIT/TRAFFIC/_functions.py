import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..', '_GITHUB_')))
from _SHARED_._common_imports import *


def get_service_wideorbit_traffic():

    try:
        service = gauth.set_wide_orbit_traffic_credentials()
        #print(f"WO Traffic service created: {service}")
    except Exception as err:
        print(f"An error occurred setting service credentials: {err}")
        
    return service

def get_stations():
    
# Load credentials from the JSON file
    service = get_service_wideorbit_traffic()

    # Define the API endpoint and headers
    url = "https://api.example.com/traffic-stations-list"  # Replace with the actual API endpoint
    headers = {
        "partner-id": service["partner-id"],
        "api-key": service["api_key"],  # Adjusted key name
        "agreement-key": service["agreement-key"]
    }
    pprint.pprint(url)
    pprint.pprint(headers)
    # Make the GET request
    #response = requests.get(url, headers=headers)

    # Check if the request was successful
    """
    if response.status_code == 200:
        stations = response.json()
        for station in stations:
            print(f"Station ID: {station['StationId']}")
            print(f"Station Call Letters: {station['StationCallLetters']}")
            print(f"Station Name: {station['StationName']}")
            print(f"Station Main Phone: {station['StationMainPhone']}")
            print()
    else:
        print(f"Failed to retrieve stations. Status code: {response.status_code}")
        print(f"Response: {response.text}")
    """
    
def main():
    try:
        print('Gathing data...\n')
        #results = get_service_wideorbit_traffic()
        results = get_stations()
        #print(results)
        print('successful test')
    except Exception as err:
        print(f"An error occurred getting data: {err}")

if __name__ == '__main__':
    main()

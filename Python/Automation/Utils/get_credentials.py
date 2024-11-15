import json
import os


def get_credentials(api_name):
    # Construct the path to the JSON file
    file_path = os.path.join("../__PRIVATE__/api_accounts.json")

    # Read the credentials from the JSON file
    with open(file_path, "r") as file:
        credentials = json.load(file)
        credentials = credentials.get(api_name, [None])[0]
        if credentials is not None:
            client_id = credentials.get("Client_ID")
            client_secret = credentials.get("Client_Secret")
            redirect_uri = credentials.get("redirect_uri")
            code = credentials.get("code")
            return client_id, client_secret, redirect_uri, code
        else:
            print("No credentials found in the file.")
            return None

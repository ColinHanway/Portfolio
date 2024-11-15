"""Api Test for NinjaOne"""

import base64
from email.utils import formatdate
import hashlib
import hmac
import requests
import pandas as pd
import urllib.request

from api_keys import NINJA_ACCESS_KEY_ID, NINJA_SECRET_ACCESS_KEY

# Credentials
API_URL = "https://api.ninjarmm.com"
CUSTOMERS_PATH = "/v1/customers"
DEVICES_PATH = "/v1/devices"
ORGANIZATIONS_PATH = "/v2/organizations-detailed"
LOCATIONS_PATH = "/v2/locations"


def request(use_path):
    # Date in RFC 2616

    """
    Make a request to the NinjaOne API, with the given path.

    The request is signed with the given secret access key.

    Returns a JSON response from the API, or raises a ValueError if the
    response code is not 200.

    :param use_path: The path to query, relative to :data:`API_URL`.
    :type use_path: str
    :return: The JSON response from the API.
    :rtype: dict
    :raises ValueError: If the response code is not 200.
    """
    date_str = formatdate(timeval=None, localtime=False, usegmt=True)

    http_verb = "GET"
    content_md5 = ""  # GET Requests don't normally have a body or type
    content_type = ""
    canonicalized_resource = use_path

    string_to_sign = f"{http_verb}\n{content_md5}\n{content_type}\n{date_str}\n{canonicalized_resource}"

    # Base64 encode the UTF-8 string to sign
    utf8_encoded_string_to_sign = string_to_sign.encode("utf-8")
    base64_encoded_string_to_sign = base64.b64encode(
        utf8_encoded_string_to_sign
    ).decode("utf-8")

    # Create the HMAC-SHA1 signature using the Secret Access Key
    hmac_key = bytes(NINJA_SECRET_ACCESS_KEY, "utf-8")
    message = base64_encoded_string_to_sign.encode("utf-8")
    signature = hmac.new(hmac_key, message, hashlib.sha1).digest()

    # Base64 encode the signature
    signature_base64 = base64.b64encode(signature).decode()

    auth_header = f"NJ {NINJA_ACCESS_KEY_ID}:{signature_base64}"

    headers = {"Authorization": auth_header, "Date": date_str}

    url = f"{API_URL}{use_path}"
    response = requests.get(url, headers=headers, timeout=200)

    if response.status_code == 200:
        return response.json()

    raise ValueError(f"{response.status_code} - {response.text}")


class organization:
    def __init__(self, org_dict):
        self.org_dict = org_dict
        self.org_name = self.org_dict["name"]
        self.org_node_approval_mode = self.org_dict["nodeApprovalMode"]
        self.org_id = self.org_dict["id"]
        self.org_locations = [self.org_dict["locations"]]
        self.org_policies = self.org_dict["policies"]
        self.org_settings = self.org_dict["settings"]
        for self.location in self.org_locations:
            for self.item in self.location:
                self.item["installer"] = request(
                    f"/v2/organization/{self.org_id}/location/{self.item["id"]}/installer/WINDOWS_MSI"
                )  # return f"/v2/organization/{self.org_name}/location/{location["id"]}/installer/WINDOWS_MSI"

    def __str__(self):
        return f"{self.org_name} --> {self.org_locations}"

    def __iter__(self):
        yield from self.org_id

    def get_org_dict(self):
        return self.org_dict

    def get_org_name(self):
        return self.org_name

    def get_org_approval_mode(self):
        return self.org_node_approval_mode

    def get_org_id(self):
        return self.org_id

    def get_org_locations(self):
        return self.org_locations

    def get_org_policies(self):
        return self.org_policies

    def get_org_settings(self):
        return self.org_settings


def main():
    output_dict = {}
    output_df = pd.DataFrame()
    i = 0
    for object in request(ORGANIZATIONS_PATH):
        org = organization(object)
        for location in org.get_org_locations():
            org_name = org.get_org_name()
            for item in location:
                org_name_formatted = org_name.replace("*", "")
                url = item["installer"]["url"]
                filename = f"G:/Shared drives/Corporate IT/NinjaOne/Installers/{org_name_formatted}-{item['name']}.msi"
                urllib.request.urlretrieve(url, filename)
                # print(org_name_formatted, filename)

                i += 1
            print(f"{org_name_formatted} Complete")
    print("Fully Complete")


main()

"""Api Test for NinjaOne"""

import base64
from email.utils import formatdate
import hashlib
import hmac
import requests

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
    try:
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

    except ValueError as error:
        print(repr(error))
    except Exception as e:
        print("Uncaught error:", repr(e))

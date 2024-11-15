from api_keys import SENTINEL_ACCESS_KEY
import requests
import pprint
import json


def request(api_url) -> json:
    resource = f"https://usea1-ninjaone2.sentinelone.net/web/api/v2.1/{api_url}"
    headers = {
        "Authorization": SENTINEL_ACCESS_KEY,
        "Content-Type": "application/json",
    }
    try:
        response = requests.get(resource, headers=headers, timeout=200)
        if response.status_code != 200:
            raise ValueError(
                f"Request error: {response.status_code} \n {response.text}"
            )
        return response.json()
    except TypeError as e:
        print(repr(e))


def post(api_url, data) -> json:
    resource = f"https://usea1-ninjaone2.sentinelone.net/web/api/v2.1/{api_url}"
    headers = {
        "Authorization": SENTINEL_ACCESS_KEY,
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(resource, headers=headers, data=data, timeout=200)
        if response.status_code != 200:
            raise ValueError(
                f"Request error: {response.status_code} \n {response.text}"
            )
        return response.json()
    except TypeError as e:
        print(repr(e))


def delete(api_url, data) -> json:
    resource = f"https://usea1-ninjaone2.sentinelone.net/web/api/v2.1/{api_url}"
    headers = {
        "Authorization": SENTINEL_ACCESS_KEY,
        "Content-Type": "application/json",
    }

    try:
        response = requests.delete(resource, headers=headers, data=data)
        if response.status_code != 200:
            raise ValueError(
                f"Request error: {response.status_code} \n {response.text}"
            )
        return response.json()
    except TypeError as e:
        print(repr(e))


def request_to_json():
    response = request("sites/2038496615865219375")
    with open("example_site.json", "w") as fp:
        json.dump(response, fp)

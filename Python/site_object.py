import json
import pprint
import requests
from sentinel_request import request, post, delete
from api_keys import SENTINEL_ACCESS_KEY

with open("symsites.json") as jf:
    sites = json.load(jf)

headers = {"Accept": "application/json", "Authorization": SENTINEL_ACCESS_KEY}


class Site:
    name: str
    id: str
    accountId: str
    groups: list

    def __init__(self, site_dict) -> None:
        for key, value in site_dict.items():
            setattr(self, key, value)
        self.groups = {}

    def get_attributes(self):
        return self.__dict__

    def __iter__(self):
        # Option 1: Iterate over the attributes and their values
        for key, value in self.get_attributes().items():
            yield key, value

    def set_groups(self):
        for group in request(f"groups?siteIds={self.id}&")["data"]:
            self.groups[group["name"]] = group["id"]

    def delete_group(self, groupId) -> json:
        return delete(f"groups/{groupId}", "")

    def get_group_policy(self, groupId):
        return request(f"groups/{groupId}/policy")


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

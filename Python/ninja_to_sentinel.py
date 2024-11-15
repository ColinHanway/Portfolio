import ninja_request
import sentinel_request
import pprint
from test import generate_json
from create_site import create_site


# pprint.pprint(sentinel_response)
ninja_names = set()
sentinel_names = set()
combined_set = set()


def get_ninja_orgs():
    ninja_response = ninja_request.request(ninja_request.ORGANIZATIONS_PATH)
    for org in ninja_response:
        thisname = org["name"]
        thisname = thisname.replace("*", "")
        ninja_names.add(thisname)
    return ninja_names


def get_sentinel_sites():
    sentinel_response = sentinel_request.request("sites?limit=100")
    for site in sentinel_response["data"]["sites"]:
        thisname = site["name"]
        thisname = thisname.replace("*", "")
        sentinel_names.add(thisname)
    return sentinel_names


def get_sentinel_no_site():
    this_sentinel_names = get_sentinel_sites()
    this_ninja_names = get_ninja_orgs()
    pprint.pprint(this_sentinel_names)
    pprint.pprint(this_ninja_names)
    sentinel_no_site = this_ninja_names - this_sentinel_names
    return sentinel_no_site


def get_sentinel_site_config():
    sentinel_response = sentinel_request.request("sites/2038496615865219375")
    site_config = sentinel_response
    site_config["data"]["name"] = "TEST"
    return site_config


def set_sentinel_site():
    example = generate_json()

    sentinel_request.post("sites", get_sentinel_site_config())


for name in get_sentinel_no_site():
    print(name, "col")
    # print(create_site(name))

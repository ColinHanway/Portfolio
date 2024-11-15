import pprint
from sentinel_request import request, post
from site_object import Site, bcolors
import json

sites = {}


def get_account_id() -> str:
    response = request("user?")
    return response["data"]["id"]


def get_sites() -> dict:
    response = request("sites?limit=100")
    sites = {}
    for item in response["data"]["sites"]:
        s = Site(item)
        sites[item["id"]] = s
    return sites


sites = get_sites()


def get_groups() -> dict:
    for ids, obj in sites.items():
        groups = []
        response = request(f"groups?siteIds={ids}&limit=100")
        response = response["data"]
        for group in response:
            groups.append(group["name"])
        sites[ids] = groups
        obj.set_groups(groups)
    return sites


def create_groups():
    for site, groups in get_groups().items():
        # Boolean flags to check if each group exists
        office = "OFFICE" in groups
        studio = "STUDIO" in groups
        broadcast = "BROADCAST" in groups
        automation = "AUTOMATION" in groups
        servers = "SERVERS" in groups

        # Check if all groups exist
        if office and studio and broadcast and automation and servers:
            print(f"Site {site} has all groups.")
        else:
            # Define the group creation logic in a helper function
            def create_group(group_name, site_id):
                body = json.dumps(
                    {"data": {"inherits": True, "name": group_name, "siteId": site_id}}
                )
                try:
                    response = post("groups", body)
                    print(
                        f"Created group '{group_name}' for site {site_id}: {response}"
                    )
                except ValueError as e:
                    print(
                        f"Failed to create group '{group_name}' for site {site_id}. Error: {str(e)}"
                    )

            # Create missing groups
            if not office:
                create_group("OFFICE", site)
            if not studio:
                create_group("STUDIO", site)
            if not broadcast:
                create_group("BROADCAST", site)
            if not automation:
                create_group("AUTOMATION", site)
            if not servers:
                create_group("SERVERS", site)


def delete_groups():
    for site, obj in sites.items():
        obj.set_groups()
        # print(obj.name, obj.id, obj.groups)
        # if "Test" in obj.groups:
        #     print(bcolors.WARNING, obj.name, obj.groups["Test"])
        #     pprint.pprint(obj.delete_group(obj.groups["Test"]))
        print(type(site))
        try:
            print(obj.groups["OFFICE"])
            pprint.pprint(obj.get_group_policy(f"{obj.groups["OFFICE"]}"))
        except KeyError as e:
            print(bcolors.FAIL + repr(e))
        except ValueError as e:
            print(bcolors.FAIL + repr(e))


get_groups()
# delete_groups()
# create_groups()
# pprint.pprint(get_groups())

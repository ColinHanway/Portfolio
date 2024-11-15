import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '_GITHUB_')))
from _SHARED_._common_imports import *

def search_groups_by_search_terms():
    groups = gw.get_groups()

    countAll = 0
    
    search_terms = [
        'all staff',
        'all users',
        'all employees'
        # Add more search terms as needed
        ]
    
    matching_groups = []  # Array to store matching groups

    for group in groups:
        name = group.get('name')
        email = group.get('email')
        members_count = group.get('directMembersCount')

        if (email and members_count is not None) and name and any(term in name.lower() for term in search_terms):
            matching_groups.append({'email': email, 'members_count': members_count})
            countAll += 1
        
    return countAll, matching_groups

def main():

    try:
        countAll, matching_groups = search_groups_by_search_terms()

        if matching_groups is not None:
            print(f"Total countAll: {countAll}")
            print("Matching Groups:")
            for group in matching_groups:
                print(f"Email: {group['email']}, Members Count: {group['members_count']}")
                
    except Exception as err:
        print(f"An error occurred getting groups: {err}")

    
if __name__ == '__main__':
    main()

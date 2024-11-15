import sys
import os

parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_directory)

print(sys.path)

from _SHARED_._common_imports import ninjutsu


orgs = ninjutsu.get_all_organizations()
print(orgs, type(orgs))

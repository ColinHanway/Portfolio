### GLOBAL IMPORTS ###
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *

### LOCAL IMPORTS ###
import gamadv as gam 

def offboarding_set_autoreply(old_email, new_email, start_date=None, end_date=None):

    if start_date is None:
        start_date = datetime.datetime.now().strftime('%Y-%m-%d')
        
    gam user john.doe@example.com vacation on
    gam user john.doe@example.com vacation set 
        subject "Auto reply" 
        message "John Doe is no longer with the company. For assistance, please contact support@example.com." 
        start start_date 
        end end_date

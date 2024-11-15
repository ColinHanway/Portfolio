### GLOBAL IMPORTS ###
import sys, os,base64
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..', '..', '_GITHUB_')))

from _SHARED_._common_imports import *
from _SHARED_._common_functions import *


API_KEY = 'l7406a31bbe06a492abd9839cdfaa88c6b'
API_SECRET = '6dcc8aea65814ac78b7cb470f562a093'

url = "https://apis-sandbox.fedex.com"

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Basic {base64.b64encode(f'{API_KEY}:{API_SECRET}'.encode()).decode()}"
}
data = {"grant_type": "client_credentials"}

response = requests.post(url, headers=headers, data=data)
response.raise_for_status()  # Raise exception if authentication fails
print(response.text)

access_token = response.json()["access_token"]
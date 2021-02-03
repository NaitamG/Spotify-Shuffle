import requests
import os
import base64
import datetime
from urllib.parse import urlencode
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv()) # This is to load your API keys from .env

token_url = "https://accounts.spotify.com/api/token" # url to get authorization and make a token for a session
method = "POST"

# set the credentials from .env file
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')

# make an f string with the credentials, which will be encoded with base64 later
client_creds = f"{client_id}:{client_secret}"

# this encodes the creds into bytes and then one more time into base64 for it to be passed in header
client_creds_b64 = base64.b64encode(client_creds.encode())


token_data = {
    "grant_type": "client_credentials",
}

token_header = {
    "Authorization": f"Basic {client_creds_b64.decode()}" # client credentials utilized for authorization, creds are decoded to make it into a base64 encoded string not bytes 
}

response = requests.post(token_url, data=token_data, headers=token_header)

# handling the initial authentication requests
if response.status_code in range(200, 299): # to check if the response is valid or not
    
    response_data = response.json() # returns a map of different auth data
    
    now = datetime.datetime.now()
    access_token = response_data['access_token'] # grab the access_token
    expires_in = response_data['expires_in'] # grab the expire_in value, time in seconds
    
    expires = now + datetime.timedelta(seconds=expires_in)
    did_it_expire = expires < now # keep a bool value to check if session is expired or not
    #print(response_data)
    
    
    
    
# this is the browser API requests, using the access key and url to search the new release data
headers = {
    "Authorization" : f"Bearer {access_token}" # use the access token from above
}

endpoint = "https://api.spotify.com/v1/browse/new-releases" # endpoint to use for browser api
data = urlencode({"country": "US", "limit": "25"})
lookup_url = f"{endpoint}?{data}" # final url that'll be used

browser_response = requests.get(lookup_url, headers=headers) # make the request
browser_data = browser_response.json()

for i in range(0, 25):
    print(browser_data['albums']['items'][i]['name'])
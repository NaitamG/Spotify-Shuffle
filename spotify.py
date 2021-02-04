import requests
import os
import base64
#import datetime
from urllib.parse import urlencode
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template

# different lists that will be used to store data
artist=[]
songs=[]
artists_img=[]
song_img=[]
preview_url=[]
artist_data=[]


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
    
    #now = datetime.datetime.now()
    access_token = response_data['access_token'] # grab the access_token
    #expires_in = response_data['expires_in'] # grab the expire_in value, time in seconds
    
    #expires = now + datetime.timedelta(seconds=expires_in)
    #did_it_expire = expires < now # keep a bool value to check if session is expired or not
    #print(response_data)
    

# this will get the song name, artists, images, url... using the tracks API
headers = {
    "Authorization" : f"Bearer {access_token}" # use the access token from above
}

# the artist's id
artist_id = ['0Y5tJX1MQlPlqiwlOH1tJY', '50co4Is1HCEo8bhOyUWKpn', '3MZsBdqDrRTJihTHQrO6Dq', '4O15NlyKLIASxsJ0PrXPfz', '3TVXtAsR1Inumwj472S9r4', '1anyVhU62p31KFi8MEzkbf', '7tYKF4w9nC0nq9CsPZTHyP', '2h93pZq0e7k5yf4dywlkpM'] 
# travis, young thug, joji, lil uzi, drake, chance, sza, frank ocean

for i in artist_id:
    
    endpoint = f"https://api.spotify.com/v1/artists/{i}/top-tracks" # endpoint to use for artists' top-tracks api
    market = urlencode({"market": "US"})
    lookup_url = f"{endpoint}?{market}"
    artist_response = requests.get(lookup_url, headers=headers) # make the request
    
    artist_data.append(artist_response.json()) # append each artist's data into the list 

# since there's lack of consistency in the data, these are the specific indicies used to get that song/name
indicies = {
    "artist_indicies": [0,-1,0,0,0,0,0,0],
    "song_indicies": [4,4,0,9,3,4,3,0]
}

for i in range(0, len(artist_data)):
    artist.append(artist_data[i]['tracks'][0]['artists'][indicies['artist_indicies'][i]]['name'])
    songs.append(artist_data[i]['tracks'][indicies['song_indicies'][i]]['name'])
    song_img.append(artist_data[i]['tracks'][indicies['song_indicies'][i]]['album']['images'][1]['url'])
    preview_url.append(artist_data[i]['tracks'][indicies['song_indicies'][i]]['preview_url'])
    
"""for i in range(0, len(artist_data)):
    print(artist[i])
    print(songs[i])
    print(song_img[i])
    print(preview_url[i])"""
    
# introducing Flask framework to pass the data in list format 
    
app = Flask(__name__)

@app.route('/')
    
def spotify():
    
    return render_template(
        "index.html",
        len = len(artist_data),
        artist = artist,
        songs = songs,
        song_img = song_img,
        preview_url = preview_url
    )
    
app.run(
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0'),
    debug=True
)
#################################################################
from flask import Flask, request, url_for, session, redirect 
import spotipy 
import time 
from spotipy.oauth2 import SpotifyOAuth
import google_oauth2.credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build


app = Flask(__name__)

app.secret_key = "Sviosnfvso03423s"
app.config['SESSION_COOKIE_NAME'] = 'William Cookie'
TOKEN_INFO = "token_info" #key to get the information in the session dictonary 

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth() #create the spotify oauth
    oauth_url = sp_oauth.get_authorize_url() #get the url 
    return redirect(oauth_url) #then redirect the user on the url

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth() #create the spotify oauth
    session.clear() # clear the session we don't want to have an old session 
    code = request.args.get('code') # use the request to get the code 
    token_info = sp_oauth.get_access_token(code) # we want to get the access token of the code 
    session[TOKEN_INFO] = token_info # saving token information  
    return redirect(url_for('getTracks', _external = True))

@app.route('/getTracks')
def getTracks():
    #try:
    token_info = get_token()
    #except:
        #print("user not logged in")
       # return redirect(url_for("login", __external = False))
    sp = spotipy.Spotify(auth= token_info['access_token'])
    all_song = []
    iter = 0
    while True:
        items = sp.current_user_saved_tracks(limit = 50, offset=iter * 50)['items']
        iter += 1
        all_song += items
        if(len(items) < 50 ):
            break
    return str(len(all_song))


# when checking with the time it don't work and i don't know why thus i am keeping it like this 
# i have 1hour with the current working token thus it should be ok 
def get_token():
    token_info = session.get(TOKEN_INFO, None)
   #if not token_info: # we want it to be none
   #     raise Exception("token info is missing")
    '''now = int(time.time()) # get the current time 

    is_expired = token_info['expired_at'] - now < 60 #check if the token will expire soon
    if is_expired: #if it is we create a new one
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token']) #give the refresh token'''
    return token_info   #return the token to use it


def create_spotify_oauth():
    return SpotifyOAuth (
        client_id = "9bd2a1a7000747058f80f6d95f4bb31a",
        client_secret = "cd1105a307404b5bba44442914ff711f",
        redirect_uri = url_for('redirectPage', _external = True),
        scope = "user-library-read")
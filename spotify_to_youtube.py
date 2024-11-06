#################################################################
from flask import Flask, request, url_for, session, redirect 
import spotipy 
import time 
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

app.secret_key = "Sviosnfvso03423s"
app.config['SESSION_COOKIE_NAME'] = 'William Cookie'
TOKEN_INFO = "token_info" #key to get the information in the session dictonary 
client_id = "9bd2a1a7000747058f80f6d95f4bb31a"


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


#creer un matrice des le debut pour ensuite le faire fonctionner et l'utiliser et bien le faire  
@app.route('/getTracks')
def getTracks():
    try:
        token_info = get_token() #try to get the token 
    except:
        print("user not logged in") #if they cannot get the token we print this and redirect the user to the login page 
        return redirect(url_for('login', _external = False))
    sp = spotipy.Spotify(auth= token_info['access_token']) # retrieve the information needed in the access token 
    all_playlist = [] #do a list to store all the song
    iter = 0 
    while True: #while loop beceause the limit is 50 and if their are more music or less we have to break basicall_playlisty continue until we saw all the music 
        items = sp.current_user_playlists(limit=50, offset= iter * 50 )['items']
        iter += 1
        all_playlist += items
        if(len(items) < 50 ):
            break
    get_album_track(token_info, all_playlist)
    return str(all_playlist)


# when checking with the time it don't work and i don't know why thus i am keeping it like this 
# i have 1hour with the current working token thus it should be ok 

#no now it it working when i hard coded the url of the page i want to redirect it 
def get_token():
    token_info = session.get(TOKEN_INFO, None) #getting the token information 
    if not token_info: # we want it to be none
        raise Exception("token info is missing")
    
    now = int(time.time()) # get the current time 
    if 'expires_at' in token_info and token_info['expires_at'] - now < 60: # check if the current token will expire soon
        sp_oauth = create_spotify_oauth() #create a new object oauth
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token']) #give the refresh token
        session[TOKEN_INFO] = token_info # update the token info
    return token_info   #return the token to use it







# HERE I WANT TO CREATE A FUNCTION THAT TRAVERSE all_playlist THE PLAYLIST THAT I HAVE SAVED THEN CALL GET TRACKS ON EACH PLAYLIST 
def get_album_track(token_info, all_playlist):
    sp = spotipy.Spotify(auth= token_info['access_token']) # retrieve the information needed in the access token 
    for i in range (len(all_playlist)):
        all_song = [] #do a list to store all the song in the playlist
        playlist_id = all_playlist[i]['id']
        iter = 0
        while True: #while loop beceause the limit is 50 and if their are more music or less we have to break basicall_playlisty continue until we saw all the music 
            items = sp.playlist_items(playlist_id, limit=100, offset= iter * 100)['items']
            iter += 1
            for it in items:
                track = it['track']
                track_info = {
                    'name' : track['name'],
                    'artist': ", ".join([artist['name']for artist in track['artists']]),
                    'album' : track['album']['name'],
                    'track_id' : track['id']
                }
                all_song.append(track_info)
            if(len(items) < 100 ):
                break
        all_playlist.append( all_song)
    #return all_playlist









def create_spotify_oauth():
    redirect_uri = url_for('redirectPage', _external = True)
    print(f"redirect url {redirect_uri}")
    return SpotifyOAuth ( # creating the object we want 
        client_id = "9bd2a1a7000747058f80f6d95f4bb31a",
        client_secret = "cd1105a307404b5bba44442914ff711f",
        redirect_uri = redirect_uri,
        scope = "user-library-read")
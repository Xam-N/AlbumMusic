import flask
import urllib.parse
import webbrowser
import threading
import requests
import base64
import datetime
import apiKeys

#playlistName = "Music TBL"
playlistName = "CodeTest"

app = flask.Flask(__name__)

authCode = None

callback_event = threading.Event()

clientID = apiKeys.spotifyClientID

clientSecret = apiKeys.spotifyClientSecret

redirectURI = 'http://localhost:8888/callback'

def SpotifyTokenGen():  
  
  threading.Thread(target=lambda: app.run(port=8888)).start()

  webbrowser.open('http://localhost:8888/login')

  callback_event.wait()
  
  accessToken = getKey(authCode, redirectURI,clientID,clientSecret)['access_token']
  
  return accessToken

@app.route('/login')
def login():
    scope = 'user-read-private playlist-modify-private'
    
    query_params = urllib.parse.urlencode({
        'response_type': 'code',
        'client_id': clientID,
        'scope': scope,
        'redirect_uri': redirectURI
    })
    auth_url = f'https://accounts.spotify.com/authorize?{query_params}'
    return flask.redirect(auth_url)

@app.route('/callback')
def callback():
  global authCode
  code = flask.request.args.get('code')
  authCode = code
  callback_event.set()
  return code

def getKey(authCode,redirect_uri,clientID,clientSecret):
  url = "https://accounts.spotify.com/api/token"
  authString = clientID + ":" + clientSecret
  authString = base64.b64encode(authString.encode()).decode()
  data = {
    "code": authCode,
    "redirect_uri": redirect_uri,
    "grant_type": "authorization_code"
  }
  headers = {
    "content-type" : "application/x-www-form-urlencoded",
    "Authorization" : "Basic " + authString
  }
  response = requests.post(url, headers=headers, data=data)
  return response.json()

def getPlaylists(accessToken):
  playlistID = ""
  url = "https://api.spotify.com/v1/users/slothsinblack/playlists?limit=50"
  header = {
      "Authorization" : 'Bearer ' + accessToken,
      "Content-Type" : "application/json"
  }
  response = requests.get(url,headers = header)

  for playlist in response.json()['items']:
    #print(playlist['name'])
    if playlistName in playlist['name']:
      return playlist['id']
    
  return playlistID

def findAlbumID(accessToken, album): #maybe use this instead, sometimes he might not put the full title of the song so it might be hard to find the specific song
  url = "https://api.spotify.com/v1/search"
  params = {
    "q": album,
    "type":"album",
    "limit":"1"
  }
  header = {
    "Authorization":'Bearer '+accessToken
  }
  response = requests.get(url,params=params,headers=header)
  print(response)
  return response['items']['id']
  
def findAlbumTracks(accessToken, albumID):
  pass
  
def findSongID(songToSearch, accessToken,albumName):
  year = datetime.date.today().strftime("%Y")
  url = "https://api.spotify.com/v1/search"

  artistName, songTitle = songToSearch.split(" - ", 1) #ensures that only 1 split takes place
  if "ft." in songTitle:
    #print(f"Removing featured artists {songTitle}")
    songTitle = songTitle.split(" ft. ",1)[0]
    #print(f"Removed featured artists {songTitle}")
    
  params = {
    "q": f"track:{songTitle} artist:{artistName} year:{year} album:{albumName}",
    "type" : "track",
    "limit":"1"
  }
  header = {
    "Authorization":f"Bearer {accessToken}"
  }
  
  response = requests.get(url,params=params,headers=header)
  
  if response.json()['tracks']['total'] == '0':
    print(f"Failed to find {songTitle} {artistName}")
    return None
  
  return response



def findSongID(songToSearch, accessToken, album):
  #print(songToSearch)
  #print(album)
  songToSearch = songToSearch + " " + album
  url = "https://api.spotify.com/v1/search"
  params = {
    "q" : songToSearch,
    "type" : "track",
    "limit":"1"
  }
  header = {
    "Authorization" : 'Bearer ' + accessToken
  }
  response = requests.get(url,params=params,headers=header)
  #print(response)
  return response



def addSongToPlaylist(playlistID, songID, accessToken):
    url = f"https://api.spotify.com/v1/playlists/{playlistID}/tracks"
    headers = {
        "Authorization": "Bearer " + accessToken,
        "Content-Type": "application/json"
    }
    data = {
        "uris": [f"spotify:track:{songID}"]
    }
    response = requests.post(url, headers=headers, json=data)
    #print(response.json())
    return response
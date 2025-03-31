import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def getCredentials():
  credentials = None

  if os.path.exists("token.pickle"): #if we have stored some previous credentials, might remove the perma auth requirement
    print("Loading Credentials from File...")
    with open("token.pickle","rb") as token:
      credentials = pickle.load(token)

  if not credentials or not credentials.valid: #if pickle file does not exist, get the credentials
    if credentials and credentials.expired and credentials.refresh_token: #if credentials exist, and are expired, and thee is a refresh token
      print("Refreshing Access Token....")
      credentials.refresh(Request())
    else:
      print("Fetching New Tokens....")
      flow = InstalledAppFlow.from_client_secrets_file("youtubeJson.json",scopes=["https://www.googleapis.com/auth/youtube.force-ssl"])
      
      flow.run_local_server(port=8080, prompt = "consent", authorization_prompt_message="")
      
      credentials = flow.credentials
      
      #save credentials in pickle file for next time
      with open("token.pickle","wb") as f:
        print("Saving credentials for future use....")
        pickle.dump(credentials,f)
  
  return credentials

def getDescription(youtube,videoID):
  
  request = youtube.videos().list(part = "snippet", id = videoID)
  response = request.execute()
  response = response["items"][0]["snippet"]
  albumName = response["title"].split("ALBUM REVIEW")[0]
  return response["description"],albumName

def getSongList(videoInfo):
    videoInfo = videoInfo.splitlines()
    
    songList = [] 
    song = False

    for line in videoInfo:   
        if "FAV TRACKS: " in line: # checks if in the best tracks section
           test = line.split(", ")
           for song in test:
            if "FAV TRACKS: " in song:
                temp = song.split("FAV TRACKS: ")
                songList.append(temp[1])
            else:
                songList.append(song)
           break
       
    return songList

def deleteVideo(youtube,playlistVideoID):
  
    delete_request = youtube.playlistItems().delete(id=playlistVideoID)
    delete_request.execute()
    print(f"Deleted item with ID: {playlistVideoID}")
    return
    
def youtubeInit():
  
  youtube = build("youtube", "v3", credentials=getCredentials())
  
  return youtube

def getPlaylistVideos(youtube,albumMusicID,videoNumber):
  
  request = youtube.playlistItems().list(part="status, contentDetails", playlistId = albumMusicID, maxResults = videoNumber)

  response = request.execute()
  
  return response['items']

    
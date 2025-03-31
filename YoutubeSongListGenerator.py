import requests
import apiKeys


apiKey = apiKeys.youtubeApiKey

def getChannelID(username): # gives the channel ID
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        "part": "id",
        "forUsername": username,
        "key": apiKey
    }
    
    response = requests.get(url,params = params)

    return response.json()


def get_playlist_item_id(access_token, playlist_id, video_id): #requires me to 2auth with youtube
    url = "https://www.googleapis.com/youtube/v3/playlistItems"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "part": "id",
        "playlistId": playlist_id,
        "maxResults": 50  # Adjust if needed
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        items = response.json().get("items", [])
        for item in items:
            if item["snippet"]["resourceId"]["videoId"] == video_id:
                return item["id"]  # Return the playlist item ID
    else:
        print("Error:", response.json())

    return None



def removeVideo(accessToken, playlistItemID): #requires me to 2oath with youtube
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?id={playlistItemID}"
    headers = {"Authorization": f"Bearer {accessToken}"}

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        print("Video removed from playlist.")
    else:
        print("Error:", response.json())


def getYoutubePlaylist(channelID,playlistID):
    url = "https://www.googleapis.com/youtube/v3/playlistItems"
    params = {
        "part": "snippet",
        "playlistId": playlistID,
        "key": apiKey,
        "maxResults": 50
    }
    
    response = requests.get(url,params = params)
    return response.json()



#should change this so that I instead use all videos from my music tbl playlist
def searchForVideo(channelID,query): #requires the exact video name

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "channelID": channelID,
        "q": query,
        "key":apiKey
    }
    response = requests.get(url,params=params)
    print(response)
    vidID = response.json()["items"][0]["id"]["videoId"]
    
    return vidID

def getVideo(videoID):
    
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet",
        "id": videoID,
        "key":apiKey
    }
    response = requests.get(url, params=params)
    print(response)
    return response.json()["items"][0]["snippet"]["description"]

def SongList(channelName, albumName): # returns this weeks best tracks
        
    videoInfo = getVideo(searchForVideo(getChannelID(channelName),albumName)) # gives the description of the latest needledrop weekly video

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
  
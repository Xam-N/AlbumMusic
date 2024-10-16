import requests
import apiKeys


apiKey = apiKeys.youtubeAPIKey

def getChannelID(username): # gives the channel ID
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        "part": "id",
        "forUsername": username,
        "key": apiKey
    }
    
    response = requests.get(url,params = params)

    return response.json()

def getYoutubePlaylist(channelID,playlistID):
    url = "https://www.googleapis.com/youtube/v3/playlists"
    params = {
        "part": "contentDetails",
        "channelId": channelID,
        "id": playlistID,
        "key": apiKey
    }
    
    response = requests.get(url,params = params)

    return response.json()

channelID = getChannelID("slothsinblack5509")

playlistID = "PL32sp9oyUIP1BWRYjBgENBmhJqvc36x0S"

print(getYoutubePlaylist(channelID,playlistID))


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
  
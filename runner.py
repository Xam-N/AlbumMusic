import YoutubeSongListGenerator
import SpotifyPlaylistGenerator
import os

def runner():
  
  #print("Name of the Youtube Channel: ")
  #channelName = input()
  #print("Name of the album to review: ")
  #albumName = input()
  
  #for each video in youtube playlist
  
  

  channelID = "UCeWoyf12adY7W2DgPy79A7w"

  playlistID = "PL32sp9oyUIP1BWRYjBgENBmhJqvc36x0S"
  
  youtubePlaylistVids = []
  
  youtubePlaylist = YoutubeSongListGenerator.getYoutubePlaylist(channelID,playlistID)['items']
  
  for video in youtubePlaylist:
      snip = video['snippet']['title']
      if "Top" not in snip:
          youtubePlaylistVids.append(snip)
          
  
  print(youtubePlaylistVids)
  
  channelName = "theneedledrop"
  
  songList = []
  
  accessToken = SpotifyPlaylistGenerator.tokenGen()
  
  for video in youtubePlaylistVids:
    
    album = video.split("ALBUM REVIEW")[0]

    songList = (YoutubeSongListGenerator.SongList(channelName, video))   
    
    print(songList)
    print(album)
  
    #playlistID = SpotifyPlaylistGenerator.getPlaylists(accessToken) Playlist does not appear in playlist list
    
    playlistID = "66iZdZJ8PBkxp3C6wPAPdr"
    
  

    for song in songList:
      #print(song)
      #print(accessToken)
      #print(album)
      songID = SpotifyPlaylistGenerator.findSongID(song, accessToken,album).json()['tracks']['items'][0]['id']
      SpotifyPlaylistGenerator.addSongToPlaylist(playlistID,songID,accessToken)
  
  os._exit(0)
  

runner()
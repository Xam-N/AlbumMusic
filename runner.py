import YoutubeSongListGenerator
import SpotifyPlaylistGenerator
import os
import datetime

def runner():
  
  #print("Name of the Youtube Channel: ")
  #channelName = input()
  #print("Name of the album to review: ")
  #albumName = input()
  
  #for each video in youtube playlist
  
  

  channelName = "theneedledrop"
  vidName = "Kendrick Lamar - To Pimp A Butterfly ALBUM REVIEW"
  album = vidName.split("ALBUM REVIEW")[0]
  #album = "Kendrick Lamar - To Pimp A Butterfly"
  vidName = "Fontaines D.C. - Romance ALBUM REVIEW"
  album = vidName.split("ALBUM REVIEW")[0]
  #album = "Fontaines D.C. - Romance"
  
  
  for video in youtubePlaylist:
  
    songList = YoutubeSongListGenerator.SongList(channelName, vidName)
    
    accessToken = SpotifyPlaylistGenerator.tokenGen()
    
    #playlistID = SpotifyPlaylistGenerator.getPlaylists(accessToken) Playlist does not appear in playlist list
    
    playlistID = "66iZdZJ8PBkxp3C6wPAPdr"

    for song in songList:
      songID = SpotifyPlaylistGenerator.findSongID(song, accessToken,album).json()['tracks']['items'][0]['id']
      SpotifyPlaylistGenerator.addSongToPlaylist(playlistID,songID,accessToken)
  
  os._exit(0)
  

runner()
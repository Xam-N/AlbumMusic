import YoutubeSongList
import SpotifyPlaylistGenerator
import os


videoNumber = input("Number of videos to be added: ") #number of videos to be added - max number is 50

if input(f"Type 'Yes' if '{videoNumber}' was the intended input ") != "Yes":
  os._exit(0)

youtubeAlbumMusicPlaylistID = "PL32sp9oyUIP1BWRYjBgENBmhJqvc36x0S" #youtube playlist ID

spotifyPlaylistID = "66iZdZJ8PBkxp3C6wPAPdr" #spotify playlistID, make sure to open it on web browser as the url changes compared to the desktop version

def runner():
   
  youtubeAlbumMusicPlaylistID = "PL32sp9oyUIP1BWRYjBgENBmhJqvc36x0S"
  
  spotifyAccessToken = SpotifyPlaylistGenerator.SpotifyTokenGen()
  
  spotifyPlaylistID = "66iZdZJ8PBkxp3C6wPAPdr"
  
  youtube = YoutubeSongList.youtubeInit()

  videos = YoutubeSongList.getPlaylistVideos(youtube,youtubeAlbumMusicPlaylistID,videoNumber)

  for item in videos:
    
      videoID = item['contentDetails']['videoId'] #id of the video
      playlistVideoID = item['id'] #id of the playlist video
      
      videoInfo,AlbumName = YoutubeSongList.getDescription(youtube,videoID)
      
      goodSongs = YoutubeSongList.getSongList(videoInfo)
      
      print(AlbumName)
      print(goodSongs)
      
      
      for song in goodSongs:
        songID = SpotifyPlaylistGenerator.findSongID(song, spotifyAccessToken,AlbumName).json()['tracks']['items'][0]['id']
        SpotifyPlaylistGenerator.addSongToPlaylist(spotifyPlaylistID,songID,spotifyAccessToken)
          
      YoutubeSongList.deleteVideo(youtube,playlistVideoID)
  
  os._exit(0)
  

runner()
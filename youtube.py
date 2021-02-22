#!/usr/bin/env python3

#import pytube library, mutagen library regex library, moviepy library and system command library
from library.functions import *

if __name__ == "__main__":
#Create directory if it doesn't exist
 if not os.path.exists('music'):
  os.makedirs('music')

#EDIT THIS LINK WITH PLAYLIST OF CHOICE
 url = "https://www.youtube.com/playlist?list=PLG5z-46tZguIbGGzEKL78cLxTY52YASFs"

#What video/playlist to donwload from
 playlist = playlistSeperator(url)

#For loop of all youtuibe links in playlist
 for url in playlist.video_urls:
  tempYT = pytube.YouTube(url)

#Regex for youtube video id's
  yt_id = re.search("=.*$",url)

  print("Downloading... " + tempYT.title)
  tempYT.register_on_complete_callback(complete_download)
  file_path = tempYT.streams.get_audio_only().download('./music')

  set_album_art(file_path,yt_id.group(0))
  place = os.getcwd() + '\\music\\' + file_path[46:]
  other_info(pytube.request.get(url),place[:-1] + '3')
#import pytube library, mutagen library regex library, moviepy library and system command library
import pytube
import os
import sys
import re
import requests
from moviepy.editor import *
from mutagen.mp3 import MP3,EasyMP3
from mutagen.id3 import ID3, APIC, error

def other_info(input,file_path):
 tags = EasyMP3(file_path);

 #Setting song name
 match = re.findall(r"{\"simpleText\":\"Song\"},\"contents\":\[{\"simpleText\":\"([^\"]*)\"}",input)
 if match == None:
  title_name = file_path[44:]
  tags["title"] = title_name[:-4]
  tags.save()
  return
 else:
  #set tag as
  final_title = ""
  for x in match:
   print (x)
   final_title = final_title + x + " & "
  tags["title"] = final_title[:-3];

 #setting Artist
 match = re.search(r"{\"simpleText\":\"Artist\"},\"contents\":\[{\"simpleText\":\"([^\"]*)\"}",input)
 if match == None:
  pass
 else:
  #set tag as
  tags["artist"] = match.group(1);

 #setting Album
 match = re.search(r"{\"simpleText\":\"Album\"},\"contents\":\[{\"simpleText\":\"([^\"]*)\"}",input)
 if match == None:
  pass
 else:
  #set tag as
  tags["album"] = match.group(1);

 tags.save()
 

def set_album_art(file_path,yt_id):
 
 picture = 'http://i3.ytimg.com/vi/' + yt_id[1:] + '/hqdefault.jpg' 

 img_data = requests.get(picture).content
 
 with open('./music/temp.jpg', 'wb') as handler:
  handler.write(img_data)
 
 picture_path = './music/temp.jpg'
 audio_path = file_path[:-1] + '3'
 
 audio = MP3(audio_path, ID3=ID3)

 try:
  audio.add_tags()
 except error:
  pass

 audio.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=open(picture_path,'rb').read()))
# edit ID3 tags to open and read the picture from the path specified and assign it
 audio.save()  # save the current changes

 os.remove('./music/temp.jpg')

def complete_download(stream,file_path):
 mp4_clip = AudioFileClip(file_path)
  
 mp4_clip.write_audiofile(file_path[:-1] + '3')

 mp4_clip.close()

 os.remove(file_path)

def playlistSeperator (url):
 playlist = pytube.Playlist(url)
 playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
 return playlist

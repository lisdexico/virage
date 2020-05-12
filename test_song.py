""" Test the song class """

from virage import *

audio_url = "http://www.v-i-r-a-g-e.com/wpv/wp-content/uploads/MUSIC%20UPLOAD/+The%20George%20Kaplan%20Conspiracy%20-%20Paul's%20Jam.mp3"

song = Song(audio_url)

print(song)

print(song.name)
print(song.audio_url)
print(song.image_url)
song.download()
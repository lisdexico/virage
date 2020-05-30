""" Test the song class """

from virage import *

# Successful download
print("\n\n---------------------------------")
print("Test 1: Successful download:\n")
audio_url = "http://www.v-i-r-a-g-e.com/wpv/wp-content/uploads/MUSIC%20UPLOAD/+The%20George%20Kaplan%20Conspiracy%20-%20Paul's%20Jam.mp3"

song = Song(audio_url)
print(song.name)
print(song.audio_url)
song.download()



# Unsuccessful download
print("\n\n---------------------------------")
print("Test 2: Unsuccessful download due to bad URL:\n")
audio_url = "http://www.v-i-r-a-g-e.com/The%20George%20Kaplan%20Conspiracy%20-%20Paul's%20Jam.mp3" # Bad URL
song = Song(audio_url)
try:
    song.download()
except Exception as e:
    print(e)


# Unsuccessful save
print("\n\n---------------------------------")
print("Test 3: Unsuccessful download due to bad folder to save:\n")
audio_url = "http://www.v-i-r-a-g-e.com/wpv/wp-content/uploads/MUSIC%20UPLOAD/+The%20George%20Kaplan%20Conspiracy%20-%20Paul's%20Jam.mp3"
song = Song(audio_url)
try:
    song.download("./missing_folder")
except Exception as e:
    print(e)
""" Test the song class """

from virage import *
from bs4 import BeautifulSoup

# Get song

html = requests.get("http://www.v-i-r-a-g-e.com/page/1/?ajx=1").content

soup = BeautifulSoup(html, "html.parser")

posts = soup.find_all(class_="post newpost type-post status-publish format-audio hentry category-non-classe post_format-post-format-audio")

post = posts[0]

audio_url = post.find(class_="control play").img["alt"]

full_title = post.find(class_="entry-title").string.strip()

image_url = post.find(class_="attachment-post-thumbnail wp-post-image front")["src"]

song = Song(audio_url, full_title, image_url)

song.download()

'''


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

'''
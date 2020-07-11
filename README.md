# virage
Python script to download all the songs available at www.v-i-r-a-g-e.com

## Dependencies:
requests - pip install requests
BeautifulSoup4 - pip install beautifulsoup4
mutagen - pipi install mutagen

The script download_new.py downloads all songs (with title, artist, and album cover metadata) in the www.v-i-r-a-g-e.com except those in the file "list_of_downloaded_songs.txt". If the file is not there, it downloads all the songs found in the website. The files are saved in the folder "music", and a list of the downloaded songs is kept in the file "list_of_downloaded_songs.txt".

The script segregate.py separates the files in the "music" folder into two different subfolders according to bitrate.


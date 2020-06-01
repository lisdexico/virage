# virage
Python script to download all the songs available at www.v-i-r-a-g-e.com

Dependencies: the python module "requests".

The script download_new.py downloads all songs found in www.v-i-r-a-g-e.com except those in the file "list_of_downloaded_songs.txt". If the file is not there, it downloads all the songs found in the website. The files are saved in the folder "music", and a list of the downloaded songs is kept ins the file "list_of_downloaded_songs.txt"

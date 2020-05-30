import requests
from html.parser import HTMLParser
import concurrent.futures

class MP3Finder(HTMLParser):
    """This class finds all links to mp3 audio in an html and saves them in the list self.MP3"""

    def __init__(self):
        super().__init__()
        self.mp3 = []

    def reset(self):
        super().reset()
        self.mp3 = []

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[1].endswith(".mp3"):
                self.mp3.append(attr[1])


class Song:
    """This class represents song"""

    def __init__(self, audio_url):
        self.audio_url = audio_url
        self.__extract_name_from_url()

    def __extract_name_from_url(self):
        self.name = self.audio_url.split("/")[-1]
        self.name = self.name.replace("+", "")
        self.name = self.name.replace("%20", " ")

    def download(self, folder="."):
        # Download audio
        try:
            response = requests.get(self.audio_url)
            response.raise_for_status()
        except Exception as e:
            e.args = (f"Failed to download {self.name}", *e.args)
            raise
        
        # Save audio
        filename = f"{folder}/{self.name}"
        try:
            with open(filename, "wb") as f:
                f.write(response.content)
        except Exception as e:
            raise

        


class Virage:
    """This class will represent the v-i-r-a-g-e website and its contents"""

    def __init__(self):
        self.page = 1
        self.mp3_finder = MP3Finder()
        self.songs = []
        self.session = requests.Session()
        self.memory_file = "list_of_downloaded_songs.txt"

    def __find_songs_in_html(self, page_html):
        self.mp3_finder.reset()
        self.mp3_finder.feed(page_html)
        self.songs.extend([Song(url) for url in self.mp3_finder.mp3])

    def find_songs(self):
        print("Scanning http://v-i-r-a-g-e.com for songs")
        page = 1
        while True:
            response = self.session.get(f"http://www.v-i-r-a-g-e.com/page/{page}/?ajx=1")
            if response.status_code != 200:
                break
            self.__find_songs_in_html(response.text)
            print(f"Scanned page {page}. Found {len(self.songs)} songs so far.")
            page += 1

        print(f"\n\n Found total of {len(self.songs)} songs")

    def download_song(self, song, folder="."):
        try:
            song.download(folder=folder)
        except Exception as e:
            print(f"Failed to download and save {song.name}")
            print(e)
        else:
            print(f"Successfully downloaded {song.name} and saved it in {folder}")
            with open(self.memory_file, "a") as f:
                f.write(song.name + "\n")

    def download_songs(self, song_list, folder=".", simultaneous_downloads=10):
        """ Download songs in the list in parallel, excecuting simultaneous_downloads at a time"""
        with concurrent.futures.ThreadPoolExecutor(max_workers=simultaneous_downloads) as excecutor:
            excecutor.map(lambda song : self.download_song(song, folder=folder), self.songs)

    def download_all_songs(self, folder=".", simultaneous_downloads=10):
        self.download_songs(self.songs, folder, simultaneous_downloads)


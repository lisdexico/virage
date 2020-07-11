import requests
from bs4 import BeautifulSoup
import concurrent.futures
import mutagen
import mutagen.id3



class Song:
    """This class represents song"""

    def __init__(self, audio_url, full_title, image_url):
        self.audio_url = audio_url
        self.full_title = full_title
        self.image_url = image_url

    @property
    def artist(self):
        return self.full_title.split("–")[0].strip()

    @property
    def title(self):
        return self.full_title.split("–")[1].strip()

    def download(self, folder="."):
        # Download audio
        try:
            response = requests.get(self.audio_url)
            response.raise_for_status()
        except Exception as e:
            e.args = (f"Failed to download {self.full_title}", *e.args)
            raise
        
        # Save audio
        filename = f"{folder}/{self.full_title}.mp3"
        try:
            with open(filename, "wb") as f:
                f.write(response.content)
        except Exception as e:
            raise

        # Download image
        try:
            response = requests.get(self.image_url)
            response.raise_for_status()
        except Exception as e:
            print(f"Couldn't download album cover for {self.full_title}") # Not a fatal error

        # Access file metadata
        try:
            metadata = mutagen.id3.ID3(filename)
        except mutagen.id3.ID3NoHeaderError:
            metadata = mutagen.File(filename, easy=False)
            metadata.add_tags()
        
        # Save image and other metadata
        try:
            metadata["APIC"] = mutagen.id3.APIC(encoding=3, mime="image/jpeg", type=3, desc=u"Thumbnail", data=response.content)
            metadata['TPE1'] = mutagen.id3.TPE1(encoding=3, text=self.artist)
            metadata['TIT2'] = mutagen.id3.TIT2(encoding=3, text=self.title)
            metadata.save(filename)

        except Exception as e:
            print("Could not add metadata")

        

        
class Virage:
    """This class will represent the v-i-r-a-g-e website and its contents"""

    default_download_folder = "."    

    def __init__(self, memory_file="list_of_downloaded_songs.txt"):
        self.page = 1
        self.songs = []
        self.session = requests.Session()
        self.memory_file = memory_file

    def __find_songs_in_html(self, html_page):
        soup = BeautifulSoup(html_page, "html.parser")
        posts = soup.find_all(class_="post newpost type-post status-publish format-audio hentry category-non-classe post_format-post-format-audio")
        for post in posts:
            audio_url = post.find(class_="control play").img["alt"]
            full_title = post.find(class_="entry-title").string.strip()
            image_url = post.find(class_="attachment-post-thumbnail wp-post-image front")["src"]
            self.songs.append(Song(audio_url, full_title, image_url))

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

    def download_song(self, song, folder=default_download_folder):
        """Downloads 'song', saves it in 'folder' and writes the song name in 'self.memory_file'"""
        try:
            song.download(folder=folder)
        except Exception as e:
            print(f"Failed to download and save {song.full_title}")
            print(e)
        else:
            print(f"Successfully downloaded {song.full_title} and saved it in {folder}")
            with open(self.memory_file, "a") as f:
                f.write(song.full_title + "\n")

    def download_songs(self, song_list, folder=default_download_folder, simultaneous_downloads=10):
        """ Download songs in the list in parallel, excecuting simultaneous_downloads at a time"""
        with concurrent.futures.ThreadPoolExecutor(max_workers=simultaneous_downloads) as excecutor:
            excecutor.map(lambda song : self.download_song(song, folder=folder), song_list)

    def download_all_songs(self, folder=default_download_folder, simultaneous_downloads=10):
        self.download_songs(self.songs, folder=folder, simultaneous_downloads=simultaneous_downloads)

    def download_new_songs(self, folder=default_download_folder, simultaneous_downloads=10):
        old_songs_titles = []
        try:
            with open(self.memory_file, "r") as f:
                old_songs_titles = f.read().splitlines()
        except Exception as e:
            print("No memory file found, downloading all songs")
        new_songs = [song for song in self.songs if song.full_title not in old_songs_titles]
        self.download_songs(new_songs, folder=folder, simultaneous_downloads=simultaneous_downloads)


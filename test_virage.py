""" Bajate todo de virage """

from virage import *
"""
virage = Virage()
virage.find_songs()
virage.download_all_songs()"""

old_songs_names = ["pepe", "mujica"]
songs = [Song("asd/pepe"), Song("asd/mujica"), Song("asd/alberto"), Song("asd/fernandez")]


new_songs = [song for song in songs if song.name not in old_songs_names]
for song in new_songs:
    print(song.name)
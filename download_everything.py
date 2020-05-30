from virage import *
from pathlib import Path

folder = "./music"

# Find or create folder to save files
try:
    Path(folder).mkdir(parents=True, exist_ok=True)
except Exception:
    print(f"Could not find or create folder {path}")

virage = Virage()
virage.find_songs()
virage.download_all_songs(folder=folder)
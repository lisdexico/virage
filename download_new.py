from virage import *
from pathlib import Path

folder = "./music"

# Find or create folder to save files
try:
    Path(folder).mkdir(parents=True, exist_ok=True)
except Exception:
    print(f"Could not find or create folder {path}")
    return

virage = Virage()
virage.find_songs()
print("Starting downloads...")
virage.download_new_songs(folder=folder)
print("Done.")
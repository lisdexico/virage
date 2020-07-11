
""" This script separates the music files in the folder 'folder' according to bitrate """

from mutagen.mp3 import MP3
from pathlib import Path
import os

folder = Path("music/")
hq_folder = folder / "HQ_lords"
lq_folder = folder / "LQ_peasants"

try:
    Path(hq_folder).mkdir(parents=True, exist_ok=True)
    Path(lq_folder).mkdir(parents=True, exist_ok=True)
except Exception:
    print(f"Could not find or create folders {hq_folder} and {lq_folder}")
else:
    # Find all files downloaded
    files = [folder / file for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))]


    for file in files: 
        metadata = MP3(file)
        bitrate = metadata.info.bitrate / 1000
        if bitrate < 320:
            os.rename(file, lq_folder / file.name)
        else:
            os.rename(file, hq_folder / file.name)
        print(f"{file}: {bitrate}")

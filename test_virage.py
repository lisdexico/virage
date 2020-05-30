""" Bajate todo de virage """

from virage import *

virage = Virage()
virage.find_songs()
virage.download_all_songs()

"""
        # Find or create folder to save it
        try:
            Path(folder).mkdir(parents=True, exist_ok=True)
        except Exception:
            print(f"Could not find or create folder {path}")
"""
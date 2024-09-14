import glob
import lyricsgenius
from pathlib import Path
from unicodedata import name
import re
from multiprocessing.pool import ThreadPool

# Make sure you write out a file called config.py in the top directory with an assigment like so:
# apikey = "my_genius_api_key"
from config import apikey

API_KEY = apikey
INPUT_PATTERN = "input/*.txt"
OUTPUT_DIR = "intermediate"
TIMEOUT = 15
RETRIES = 30
MAX_SONGS = 2

def fetchArtistSongs(artist_name):
    if len(artist_name) > 0:
        artist = genius_api.search_artist(artist_name, max_songs=MAX_SONGS)
        print(f"Populating file: {artist.name.strip()}")
        f = open(Path(OUTPUT_DIR, f'{artist.name.strip()}.txt'), 'w', encoding='utf-8')  
        for song in artist.songs:
            try:
                f.write("\n" + '*'*50 + "\n")                      
                f.write(f"{song.title} by {artist.name.strip()}\n")
                the_lyrics = song.lyrics
                ''.join(the_lyrics.splitlines(keepends=True)[1:])
                the_lyrics = re.sub(".*Lyrics", "", the_lyrics)
                the_lyrics = re.sub("\d*Embed$", "", the_lyrics)
                f.write(the_lyrics)
            except Exception as e:
                print(f"caught exception, skipping song {song}")
        f.close()
        print(f"done with {artist_name}")

#it loads rapper's names from the filename and then downloads all of their songs
genius_api = lyricsgenius.Genius(API_KEY, timeout=TIMEOUT, retries=RETRIES)
genius_api.response_format = 'plain'
input_file_list = glob.glob(INPUT_PATTERN)
print("Got file list " + str(input_file_list))

for file_name in input_file_list:
    with open(file_name) as f:
        with ThreadPool(5) as pool:
            for result in pool.imap_unordered(fetchArtistSongs, [line.strip() for line in f.readlines()]):
                pass
        #for artist_name in [line.strip() for line in f.readlines()]:
        #    fetchArtistSongs(artist_name)

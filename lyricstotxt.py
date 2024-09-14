import glob
import re
from langdetect import detect

"""
this script gives the text <bos> and <eos> tokens it could have all been one script but yeah
the foldername is passed and an argument when calling the script
"""

INPUT_PATTERN = "intermediate/*.txt"
OUTPUT_FILE = "output/corpus.txt"
MIN_SONG_LENGTH = 400

STOP_WORDS = ["discography", "highest to lowest", "radio edit", \
            "charitable work", "open letter to fan", "open letter to young", \
            "open letter to paul", "rant by kanye", "reddit ama",\
            "(clean) by"]

header = ['text']
songsfile = open(OUTPUT_FILE, 'w', encoding='utf-8')
input_file_list = glob.glob(INPUT_PATTERN)
print("Got file list " + str(input_file_list))

count = 0
for file_name in input_file_list:
    print(file_name)
    textsfile = open(file_name, encoding='utf-8')
    texts = textsfile.read()
    texts = texts.split('*'*50)
    texts = texts[1:]
    for text in texts:
        if (len(text) > MIN_SONG_LENGTH) & (not any([x in text.lower() for x in STOP_WORDS])):
            detected_language = "none"
            try:
                detected_language = detect(text)
            except Exception as e:
                print(f"Caught exception detecting language: {str(e)}")

            if detected_language == "en":
                count = count + 1
                text = re.sub("\|\|Verse 1\|\|", "[Verse 1]", text)
                text = re.sub("\|\|Verse 2\|\|", "[Verse 2]", text)
                text = re.sub("\|\|Chorus\|\|", "[Chorus]", text)
                text = re.sub("You might also like", "", text)
                text = re.sub("See.*LiveGet tickets as low as \$\d*", "", text)
                #text_with_tokens = f"\n<BOS>\n{text}\n<EOS>\n"
                text_with_tokens = f"\n{text}\n<|endoftext|>\n"
                songsfile.write(text_with_tokens)
print(count)
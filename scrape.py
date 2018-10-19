import sys
import time
from selenium import webdriver
from bs4 import BeautifulSoup

from database import create_database_connection, upload_set

# Establish Database connection
try:
    conn = create_database_connection()
except Exception as e:
    print(e)
    sys.exit()

# Create browser
driver = webdriver.Chrome()
driver.implicitly_wait(30)

# Scrape tracks
with open('queue.txt') as f:
    for line in f:
        url = line.strip()

        if(url == ""):
            print("Please populate the queue.txt")
            sys.exit()

        print("Scraping %s:" % url)

        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Scrape meta info
        source = url
        set_name = soup.find("meta", {"itemprop": "name"})["content"]
        dj_name = soup.select("#pageNavi > span")[1].text

        # Scrape Songs
        songs = []
        songs_html = soup.select("tr.tlpItem")
        for song in songs_html:

            artist_name = song.find(
                "meta", {"itemprop": "byArtist"}
            )["content"]

            song_name = song.find(
                "meta", {"itemprop": "name"}
            )["content"].split("-")[1].strip()

            try:
                label = song.find("meta", {"itemprop": "publisher"})["content"]
            except Exception:
                label = None

            try:
                duration_info = song.find(
                    "meta", {"itemprop": "duration"}
                )["content"].replace("PT", "")

                duration_min = int(duration_info.split("M")[0])
                duration_sec = int(duration_info.split("M")[1]
                                                .replace("S", ""))

                duration = duration_min * 60 + duration_sec
            except Exception:
                duration = None

            songs.append({
                "artist": artist_name,
                "title": song_name,
                "duration": duration,
                "label": label
            })

        # Add info to database
        upload_set(conn, dj_name, set_name, source, songs)
        time.sleep(5)

# Clear queue.txt & close browsers
print("Scraped queue.txt")
driver.quit()
open("queue.txt", 'w').close()

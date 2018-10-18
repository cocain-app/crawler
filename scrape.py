import re
import os
import sys
import time
import psycopg2
from selenium import webdriver
from bs4 import BeautifulSoup

# Check for secrets
if(not('DATABASE_HOST' in os.environ and
       'DATABASE_PORT' in os.environ and
       'DATABASE_USER' in os.environ and
       'DATABASE_PASSWORD' in os.environ and
       'DATABASE_DATABASE' in os.environ)):
    print("Environment variables missing.")
    sys.exit()


# Connect to database
try:
    conn = psycopg2.connect(
        "dbname='%s' user='%s' host='%s' password='%s'" %
        (
            os.environ["DATABASE_DATABASE"],
            os.environ["DATABASE_USER"],
            os.environ["DATABASE_HOST"],
            os.environ["DATABASE_PASSWORD"],
        )
    )
    cursor = conn.cursor()

    # Initialize database
    sql_file = open("init.sql", "r")
    cursor.execute(sql_file.read())
    conn.commit()

    print("Connected and initialized database")

except e:
    print("Database connection not possibe.")
    sys.exit()


# Database Functions
def get_song_id(song_title):
    SQL = "SELECT id FROM Songs WHERE title=%s"
    data = (song_title, )
    cursor.execute(SQL, data)
    records = cursor.fetchone()
    if(records is None or len(records) < 1):
        return None
    return records[0]


def create_song(song_title, artist_id, duration):
    SQL = "INSERT INTO Songs (title, artist_id, duration) VALUES (%s, %s, %s) RETURNING id;"
    data = (song_title, artist_id, duration, )
    cursor.execute(SQL, data)
    id = cursor.fetchone()[0]
    conn.commit()

    print("Added song: %s" % song_title)
    return id


def create_transition(song_from_id, song_to_id, set_id):
    SQL = "INSERT INTO Transitions (song_from, song_to, set_id) VALUES (%s, %s, %s)"
    data = (song_from_id, song_to_id, set_id, )
    cursor.execute(SQL, data)
    conn.commit()
    print("Added transition: %s-%s" % (song_from_id, song_to_id))


def get_set_id(source):
    SQL = "SELECT id FROM Sets WHERE source=%s"
    data = (source, )
    cursor.execute(SQL, data)
    records = cursor.fetchone()
    if(records is None or len(records) < 1):
        return None
    return records[0]


def create_set(source, dj_id):
    SQL = "INSERT INTO Sets (dj_id, source) VALUES (%s, %s) RETURNING id;"
    data = (dj_id, source, )
    cursor.execute(SQL, data)
    id = cursor.fetchone()[0]
    conn.commit()

    print("Added Set: %s" % source)
    return id


def get_artist_id(artist_name):
    SQL = "SELECT id FROM Artists WHERE name=%s"
    data = (artist_name, )
    cursor.execute(SQL, data)
    records = cursor.fetchone()
    if(records is None or len(records) < 1):
        return None
    return records[0]


def create_artist(artist_name):
    SQL = "INSERT INTO Artists (name) VALUES (%s) RETURNING id;"
    data = (artist_name, )
    cursor.execute(SQL, data)
    id = cursor.fetchone()[0]
    conn.commit()

    print("Added artist: %s" % artist_name)
    return id


def get_dj_id(dj_name):
    SQL = "SELECT id FROM Djs WHERE name=%s"
    data = (dj_name, )
    cursor.execute(SQL, data)
    records = cursor.fetchone()
    if(records is None or len(records) < 1):
        return None
    return records[0]


def create_dj(dj_name):
    SQL = "INSERT INTO Djs (name) VALUES (%s) RETURNING id;"
    data = (dj_name, )
    cursor.execute(SQL, data)
    id = cursor.fetchone()[0]
    conn.commit()

    print("Added dj: %s" % dj_name)
    return id


def upload_set(dj, set_name, source, songs):
    dj_id = get_dj_id(dj)
    if dj_id is None:
        dj_id = create_dj(dj)

    set_id = get_set_id(source)
    if set_id is None:
        set_id = create_set(source, dj_id)

        for index, song in enumerate(songs):
            artist_id = get_artist_id(song["artist"])
            if artist_id is None:
                artist_id = create_artist(song["artist"])

            song_id = get_song_id(song["title"])
            if song_id is None:
                # TODO: add duration
                song_id = create_song(song["title"], artist_id, 0)

            if index > 0 and index < len(songs) - 1:
                song_from_id = get_song_id(songs[index - 1]["title"])
                song_to_id = song_id
                create_transition(song_from_id, song_to_id, set_id)

    else:
        print("Already scraped set from %s" % source)


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
        dj_name = soup.select("#pageNavi > span a")[0].text

        # Scrape Songs
        songs = []
        songs_html = soup.select("tr.tlpItem")
        for song in songs_html:
            artist_name = song.find("meta", {"itemprop": "byArtist"})["content"]
            song_name = song.find("meta", {"itemprop": "name"})["content"].split("-")[1].strip()

            # label = song.find("meta", {"itemprop": "publisher"})["content"]

            # duration_info = song.find("meta", {"itemprop": "duration"})["content"].replace("PT", "")
            # duration_min = int(duration_info.split("M")[0])
            # duration_sec = int(duration_info.split("M")[1].replace("S", ""))
            # duration = duration_min * 60 + duration_sec

            songs.append({
                "artist": artist_name,
                "title": song_name,
                # "duration": duration,
            })

        # Add info to database
        upload_set(dj_name, set_name, source, songs)
        time.sleep(5)

print("Scraped queue.txt")

# Clear queue.txt
open("queue.txt", 'w').close()

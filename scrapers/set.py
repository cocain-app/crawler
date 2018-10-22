import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_set(html, url):
    soup = BeautifulSoup(html, "html.parser")

    # Scrape meta info
    set_title = soup.find("meta", {"itemprop": "name"})["content"]
    dj_name = soup.select("#pageNavi > span")[1].text

    # Scrape occasion
    try:
        occasion = soup.body.findAll(
            text=' Open Air / Festival '
        )[0].parent.parent.find_previous_sibling().select("a")[0].text
    except Exception as e:
        occasion = None

    # Scrape venue
    try:
        venue = soup.body.findAll(
            text=' Event Location '
        )[0].parent.parent.find_previous_sibling().select("a")[0].text
    except Exception as e:
        venue = None

    # Scrape next & previous setlist links
    try:
        previous_setlist = urljoin(
            url,
            soup.body.findAll(
                text='Previous Tracklist'
            )[0].parent.parent.find_next_sibling().select("a")[0].get('href')
        )
    except Exception as e:
        previous_setlist = None

    try:
        next_setlist = urljoin(
            url,
            soup.body.findAll(
                text='Next Tracklist'
            )[0].parent.parent.find_next_sibling().select("a")[0].get('href')
        )
    except Exception as e:
        next_setlist = None

    # Scrape other links
    artist_links = []
    for link in soup.body.select(".aMenu .aMenuItem.collapse a.sideLink"):
        artist_links.append(urljoin(url, link.get('href')))

    related_links = []
    for link in soup.body.select(".headBG + .aMenuItem .sideTLDiv a.sideLink"):
        related_links.append(urljoin(url, link.get('href')))

    # Scrape Songs
    songs = []
    songs_html = soup.select("tr.tlpItem")
    for song in songs_html:

        track_full = song.select(".trackValue")[0].text

        if("ID" in track_full):
            songs.append(None)
            continue

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

    # Create & return set object
    set = {
        "set_title": set_title,
        "source": url,
        "dj_name": dj_name,
        "songs": songs,
        "next_set": next_setlist,
        "previous_set": previous_setlist,
        "artist_links": artist_links,
        "related_links": related_links,
        "occasion": occasion,
        "venue": venue,
        "timestamp": time.time()
    }
    return set

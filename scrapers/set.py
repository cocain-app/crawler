from bs4 import BeautifulSoup


def scrape_set(html, url):
    soup = BeautifulSoup(html, "html.parser")

    # Scrape meta info
    set_title = soup.find("meta", {"itemprop": "name"})["content"]
    dj_name = soup.select("#pageNavi > span")[1].text

    # Scrape links
    try:
        previous_setlist = soup.body.findAll(
            text='Previous Tracklist'
        )[0].parent.parent.find_next_sibling().select("a")[0].get('href')
    except Exception as e:
        next_setlist = None

    try:
        next_setlist = soup.body.findAll(
            text='Next Tracklist'
        )[0].parent.parent.find_next_sibling().select("a")[0].get('href')
    except Exception as e:
        next_setlist = None

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

    # Create & return set object
    set = {
        "set_title": set_title,
        "source": url,
        "dj_name": dj_name,
        "songs": songs,
        "next_setlist": next_setlist,
        "previous_setlist": previous_setlist
    }
    return set

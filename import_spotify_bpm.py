import time

from database import create_database_connection
from database.song import set_song_spotify_bpm
from functions.spotify import fetch_bpms


def chunks(l, chunks):
    return zip(*[iter(l)]*chunks)


if __name__ == "__main__":
    conn = create_database_connection()

    cursor = conn.cursor()
    SQL = "SELECT id, spotify_uri FROM Songs WHERE spotify_uri IS NOT NULL"
    cursor.execute(SQL)
    records = cursor.fetchall()

    uris = []
    for song in records:
        uris.append(song[1])

    chunks = chunks(uris, 50)

    for chunk_index, chunk in enumerate(chunks):
        bpms = fetch_bpms(chunk)

        for index, bpm in enumerate(bpms):
            id = records[chunk_index * 50 + index][0]
            set_song_spotify_bpm(conn, id, bpm)

        time.sleep(2)

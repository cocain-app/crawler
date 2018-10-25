import time

from database import create_database_connection
from database.spotify import set_spotify_song_features
from functions.spotify import fetch_spotify_audio_features


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
        audio_features = fetch_spotify_audio_features(chunk)

        for index, audio_features in enumerate(audio_features):
            id = records[chunk_index * 50 + index][0]
            set_spotify_song_features(conn, id, audio_features)

        time.sleep(2)

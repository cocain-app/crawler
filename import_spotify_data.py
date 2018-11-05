import time

from database import create_database_connection
from database.spotify import set_spotify_song_features
from database.helpers import fetch_all
from functions.spotify import fetch_spotify_audio_features


def chunks(l, chunks):
    return zip(*[iter(l)]*chunks)


if __name__ == "__main__":
    conn = create_database_connection()

    # Get unfetched spotify objects
    SQL = "SELECT spotify_uri FROM Spotify_Songs WHERE tempo IS NULL"
    fetched_uris = fetch_all(conn, SQL)

    uris = []
    for object in fetched_uris:
        uris.append(object[0])

    if(len(uris) > 50):
        # Create chunks to fetch 50 at once
        chunks = chunks(uris, 50)

        for chunk_index, chunk in enumerate(chunks):
            audio_features = fetch_spotify_audio_features(chunk)

            for index, audio_features in enumerate(audio_features):
                uri = uris[chunk_index * 50 + index]

                try:
                    set_spotify_song_features(conn, uri, audio_features)
                except Exception as e:
                    print("Could not save song because of %s" % e)

            time.sleep(2)
    else:
        audio_features = fetch_spotify_audio_features(uris)
        for index, audio_features in enumerate(audio_features):
            uri = uris[index]
            set_spotify_song_features(conn, uri, audio_features)

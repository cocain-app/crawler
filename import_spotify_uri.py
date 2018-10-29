import time

from database import create_database_connection
from database.helpers import fetch_all
from database.spotify_song import create_spotify_song
from functions.spotify import fetch_song_general


if __name__ == "__main__":
    conn = create_database_connection()

    SQL = "SELECT songs.id, songs.title, artists.name FROM songs JOIN artists ON songs.artist_id = artists.id WHERE NOT EXISTS ( SELECT * from Spotify_Songs WHERE Spotify_Songs.song_id = songs.id ) GROUP BY songs.id, artists.name ORDER BY random() LIMIT 500"
    records = fetch_all(conn, SQL)

    for song in records:
        try:
            metatdata = fetch_song_general(song[1], song[2])
            create_spotify_song(conn, song[0], metatdata["uri"])
        except Exception as e:
            cursor = conn.cursor()
            cursor.execute("ROLLBACK")
            print(e)

        time.sleep(2)

import time

from database import create_database_connection
from database.song import set_song_spotify_uri
from functions.spotify import fetch_song_general


if __name__ == "__main__":
    conn = create_database_connection()

    cursor = conn.cursor()
    SQL = "SELECT songs.id, songs.title, artists.name FROM songs JOIN artists ON songs.artist_id = artists.id GROUP BY songs.id, artists.name LIMIT 500"
    cursor.execute(SQL)
    records = cursor.fetchall()

    for song in records:
        try:
            metatdata = fetch_song_general(song[1], song[2])
            set_song_spotify_uri(conn, song[0], metatdata["uri"])
        except Exception as e:
            continue

        time.sleep(2)

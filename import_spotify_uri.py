import time

from database import create_database_connection
from database.song import set_song_spotify_uri
from functions.spotify import fetch_song_general


if __name__ == "__main__":
    conn = create_database_connection()

    cursor = conn.cursor()
    SQL = "SELECT songs.id, songs.title, artists.name, count(songs.id) AS weight FROM songs JOIN artists ON songs.artist_id = artists.id INNER JOIN (SELECT song_from, song_to FROM Transitions INNER JOIN (SELECT songs.id as id FROM songs JOIN transitions on transitions.song_from = songs.id GROUP BY songs.id ORDER BY Count(songs.id) DESC LIMIT 500) AS U ON u.id = song_from) as u on u.song_from = songs.id GROUP BY songs.id, artists.name ORDER BY weight DESC LIMIT 500"
    cursor.execute(SQL)
    records = cursor.fetchall()

    for song in records:
        try:
            metatdata = fetch_song_general(song[1], song[2])
            set_song_spotify_uri(conn, song[0], metatdata["uri"])
        except Exception as e:
            continue

        time.sleep(2)

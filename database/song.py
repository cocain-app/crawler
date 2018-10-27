from .helpers import fetch_one, create_and_return_id


def get_song_id(conn, song_title, artist_id):
    SQL = "SELECT songs.id FROM Songs INNER JOIN artists ON artists.id=songs.artist_id WHERE songs.title=%s AND artists.id=%s"
    data = (song_title, artist_id, )
    return fetch_one(conn, SQL, data)


def create_song(conn, song_title, artist_id, duration):
    SQL = "INSERT INTO Songs (title, artist_id, duration) VALUES (%s, %s, %s) RETURNING id;"
    data = (song_title, artist_id, duration, )
    id = create_and_return_id(conn, SQL, data)

    print("Added song: %s" % song_title)
    return id

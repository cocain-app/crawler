from .helpers import create_and_return_id


def create_spotify_song(conn, song_id, spotify_uri):
    SQL = "INSERT INTO Spotify_Songs (spotify_uri, song_id) VALUES (%s, %s) RETURNING spotify_uri;"
    data = (spotify_uri, song_id, )
    id = create_and_return_id(conn, SQL, data)

    print("Added spotify song for %s" % song_id)
    return id

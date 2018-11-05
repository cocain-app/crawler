from .helpers import create_and_return_id


def create_spotify_song(conn, song_id, metadata):
    SQL = "INSERT INTO Spotify_Songs (spotify_uri, song_id, preview_url, image_url_small, image_url_large) VALUES (%s, %s, %s, %s, %s) RETURNING spotify_uri;"
    data = (metadata["uri"], song_id, metadata["preview_url"], metadata["image_url_small"], metadata["image_url_large"])
    id = create_and_return_id(conn, SQL, data)

    print("Added spotify song for %s" % song_id)
    return id

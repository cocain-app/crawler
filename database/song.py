def get_song_id(conn, song_title, artist_id):
    cursor = conn.cursor()
    SQL = "SELECT songs.id FROM Songs INNER JOIN artists ON artists.id=songs.artist_id WHERE songs.title=%s AND artists.id=%s"
    data = (song_title, artist_id, )
    cursor.execute(SQL, data)
    records = cursor.fetchone()
    if(records is None or len(records) < 1):
        return None
    return records[0]


def create_song(conn, song_title, artist_id, duration):
    cursor = conn.cursor()
    SQL = "INSERT INTO Songs (title, artist_id, duration) VALUES (%s, %s, %s) RETURNING id;"
    data = (song_title, artist_id, duration, )
    cursor.execute(SQL, data)
    id = cursor.fetchone()[0]
    conn.commit()

    print("Added song: %s" % song_title)
    return id


def set_song_spotify_uri(conn, song_id, uri):
    cursor = conn.cursor()
    SQL = "UPDATE Songs SET spotify_uri = %s WHERE songs.id = %s;"
    data = (uri, song_id, )
    cursor.execute(SQL, data)
    conn.commit()

    print("Updated song spotify_uri: %s %s" % (song_id, uri))

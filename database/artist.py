def get_artist_id(conn, artist_name):
    cursor = conn.cursor()
    SQL = "SELECT id FROM Artists WHERE name=%s"
    data = (artist_name, )
    cursor.execute(SQL, data)
    records = cursor.fetchone()
    if(records is None or len(records) < 1):
        return None
    return records[0]


def create_artist(conn, artist_name):
    cursor = conn.cursor()
    SQL = "INSERT INTO Artists (name) VALUES (%s) RETURNING id;"
    data = (artist_name, )
    cursor.execute(SQL, data)
    id = cursor.fetchone()[0]
    conn.commit()

    print("Added artist: %s" % artist_name)
    return id

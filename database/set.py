def get_set_id(conn, source):
    cursor = conn.cursor()
    SQL = "SELECT id FROM Sets WHERE source=%s"
    data = (source, )
    cursor.execute(SQL, data)
    records = cursor.fetchone()
    if(records is None or len(records) < 1):
        return None
    return records[0]


def create_set(conn, source, dj_id):
    cursor = conn.cursor()
    SQL = "INSERT INTO Sets (dj_id, source) VALUES (%s, %s) RETURNING id;"
    data = (dj_id, source, )
    cursor.execute(SQL, data)
    id = cursor.fetchone()[0]
    conn.commit()

    print("Added Set: %s" % source)
    return id

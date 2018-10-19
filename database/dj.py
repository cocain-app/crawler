def get_dj_id(conn, dj_name):
    cursor = conn.cursor()
    SQL = "SELECT id FROM Djs WHERE name=%s"
    data = (dj_name, )
    cursor.execute(SQL, data)
    records = cursor.fetchone()
    if(records is None or len(records) < 1):
        return None
    return records[0]


def create_dj(conn, dj_name):
    cursor = conn.cursor()
    SQL = "INSERT INTO Djs (name) VALUES (%s) RETURNING id;"
    data = (dj_name, )
    cursor.execute(SQL, data)
    id = cursor.fetchone()[0]
    conn.commit()

    print("Added dj: %s" % dj_name)
    return id

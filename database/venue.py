def get_venue_id(conn, venue_name):
    cursor = conn.cursor()
    SQL = "SELECT id FROM Venues WHERE name=%s"
    data = (venue_name, )
    cursor.execute(SQL, data)
    records = cursor.fetchone()
    if(records is None or len(records) < 1):
        return None
    return records[0]


def create_venue(conn, venue_name):
    cursor = conn.cursor()
    SQL = "INSERT INTO Venues (name) VALUES (%s) RETURNING id;"
    data = (venue_name, )
    cursor.execute(SQL, data)
    id = cursor.fetchone()[0]
    conn.commit()

    print("Added venue: %s" % venue_name)
    return id

def get_occasion_id(conn, occasion_name):
    cursor = conn.cursor()
    SQL = "SELECT id FROM Occasions WHERE name=%s"
    data = (occasion_name, )
    cursor.execute(SQL, data)
    records = cursor.fetchone()
    if(records is None or len(records) < 1):
        return None
    return records[0]


def create_occasion(conn, occasion_name):
    cursor = conn.cursor()
    SQL = "INSERT INTO Occasions (name) VALUES (%s) RETURNING id;"
    data = (occasion_name, )
    cursor.execute(SQL, data)
    id = cursor.fetchone()[0]
    conn.commit()

    print("Added occasions: %s" % occasion_name)
    return id

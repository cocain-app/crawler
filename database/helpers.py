def fetch_one(conn, sql, data):
    cursor = conn.cursor()
    cursor.execute(sql, data)
    records = cursor.fetchone()
    if(records is None or len(records) < 1):
        return None
    return records[0]


def fetch_all(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    records = cursor.fetchall()
    return records

def create_and_return_id(conn, sql, data):
    cursor = conn.cursor()
    cursor.execute(sql, data)
    id = cursor.fetchone()[0]
    conn.commit()
    return id

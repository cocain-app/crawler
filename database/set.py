from .helpers import fetch_one, create_and_return_id


def get_set_id(conn, source):
    SQL = "SELECT id FROM Sets WHERE source=%s"
    data = (source, )
    return fetch_one(conn, SQL, data)


def create_set(conn, source, dj_id, venue_id, occasion_id):
    SQL = "INSERT INTO Sets (dj_id, source, occasion_id, venue_id) VALUES (%s, %s, %s, %s) RETURNING id;"
    data = (dj_id, source, occasion_id, venue_id, )
    id = create_and_return_id(conn, SQL, data)

    print("Added Set: %s" % source)
    return id

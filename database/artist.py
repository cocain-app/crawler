from .helpers import fetch_one, create_and_return_id


def get_artist_id(conn, artist_name):
    SQL = "SELECT id FROM Artists WHERE name=%s"
    data = (artist_name, )
    return fetch_one(conn, SQL, data)


def create_artist(conn, artist_name):
    SQL = "INSERT INTO Artists (name) VALUES (%s) RETURNING id;"
    data = (artist_name, )
    id = create_and_return_id(conn, SQL, data)

    print("Added artist: %s" % artist_name)
    return id

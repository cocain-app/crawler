from .helpers import fetch_one, create_and_return_id


def get_dj_id(conn, dj_name):
    SQL = "SELECT id FROM Djs WHERE name=%s"
    data = (dj_name, )
    return fetch_one(conn, SQL, data)


def create_dj(conn, dj_name):
    SQL = "INSERT INTO Djs (name) VALUES (%s) RETURNING id;"
    data = (dj_name, )
    id = create_and_return_id(conn, SQL, data)

    print("Added dj: %s" % dj_name)
    return id

from .helpers import fetch_one, create_and_return_id


def get_venue_id(conn, venue_name):
    SQL = "SELECT id FROM Venues WHERE name=%s"
    data = (venue_name, )
    return fetch_one(conn, SQL, data)


def create_venue(conn, venue_name):
    SQL = "INSERT INTO Venues (name) VALUES (%s) RETURNING id;"
    data = (venue_name, )
    id = create_and_return_id(conn, SQL, data)

    print("Added venue: %s" % venue_name)
    return id

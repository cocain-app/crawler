from .helpers import fetch_one, create_and_return_id


def get_occasion_id(conn, occasion_name):
    SQL = "SELECT id FROM Occasions WHERE name=%s"
    data = (occasion_name, )
    return fetch_one(conn, SQL, data)


def create_occasion(conn, occasion_name):
    SQL = "INSERT INTO Occasions (name) VALUES (%s) RETURNING id;"
    data = (occasion_name, )
    id = create_and_return_id(conn, SQL, data)

    print("Added occasions: %s" % occasion_name)
    return id

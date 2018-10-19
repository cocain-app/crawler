def create_transition(conn, song_from_id, song_to_id, set_id):
    cursor = conn.cursor()
    SQL = "INSERT INTO Transitions (song_from, song_to, set_id) VALUES (%s, %s, %s)"
    data = (song_from_id, song_to_id, set_id, )
    cursor.execute(SQL, data)
    conn.commit()
    print("Added transition: %s-%s" % (song_from_id, song_to_id))

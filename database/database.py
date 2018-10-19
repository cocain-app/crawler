import os
import psycopg2

from .song import get_song_id, create_song
from .transition import create_transition
from .set import get_set_id, create_set
from .artist import get_artist_id, create_artist
from .dj import get_dj_id, create_dj


def create_database_connection():
    # Check for secrets
    if(not('DATABASE_HOST' in os.environ and
           'DATABASE_PORT' in os.environ and
           'DATABASE_USER' in os.environ and
           'DATABASE_PASSWORD' in os.environ and
           'DATABASE_DATABASE' in os.environ)):
        raise Exception("Environment variables missing.")

    # Connect
    try:
        conn = psycopg2.connect(
            "dbname='%s' user='%s' host='%s' password='%s'" %
            (
                os.environ["DATABASE_DATABASE"],
                os.environ["DATABASE_USER"],
                os.environ["DATABASE_HOST"],
                os.environ["DATABASE_PASSWORD"],
            )
        )

        print("Established Database connection")
    except Exception:
        raise Exception("Database connection not possible")

    # Initialize
    initialize_database(conn)

    return conn


def initialize_database(conn):
    cursor = conn.cursor()
    sql_file = open("init.sql", "r")
    cursor.execute(sql_file.read())
    conn.commit()


def upload_set(conn, dj_name, set_name, source, songs):
    dj_id = get_dj_id(conn, dj_name)
    if dj_id is None:
        dj_id = create_dj(conn, dj_name)

    set_id = get_set_id(conn, source)
    if set_id is None:
        set_id = create_set(conn, source, dj_id)

        for index, song in enumerate(songs):
            artist_id = get_artist_id(conn, song["artist"])
            if artist_id is None:
                artist_id = create_artist(conn, song["artist"])

            song_id = get_song_id(conn, song["title"], artist_id)
            if song_id is None:
                # TODO: add duration
                song_id = create_song(conn, song["title"], artist_id, 0)

            if index > 0 and index < len(songs) - 1:
                song_from_id = get_song_id(
                    conn,
                    songs[index-1]["title"],
                    get_artist_id(conn, songs[index-1]["artist"])
                )
                song_to_id = song_id

                create_transition(conn, song_from_id, song_to_id, set_id)

    else:
        print("Already scraped set from %s" % source)

def set_spotify_song_features(conn, song_id, audio_features):
    cursor = conn.cursor()

    acousticness = audio_features["acousticness"]
    danceability = audio_features["danceability"]
    duration_ms = audio_features["duration_ms"]
    energy = audio_features["energy"]
    instrumentalness = audio_features["instrumentalness"]
    key = audio_features["key"]
    liveness = audio_features["liveness"]
    loudness = audio_features["loudness"]
    mode = audio_features["mode"]
    speechiness = audio_features["speechiness"]
    tempo = audio_features["tempo"]
    time_signature = audio_features["time_signature"]
    valence = audio_features["valence"]

    uri = audio_features["uri"]

    SQL = "INSERT INTO Spotify_Songs (spotify_uri, song_id, acousticness, danceability, duration_ms, energy, instrumentalness, key, liveness, loudness, mode, speechiness, tempo, time_signature, valence) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );"
    data = (
        uri,
        song_id,
        acousticness,
        danceability,
        duration_ms,
        energy,
        instrumentalness,
        key,
        liveness,
        loudness,
        mode,
        speechiness,
        tempo,
        time_signature,
        valence
    )

    try:
        cursor.execute(SQL, data)
        conn.commit()
    except Exception as e:
        print("Couldn't add song. %s" % e)

    print("Added spotify song: %s %s" % (song_id, uri))

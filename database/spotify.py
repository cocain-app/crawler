def set_spotify_song_features(conn, uri, audio_features):
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

    SQL = "UPDATE Spotify_Songs SET acousticness = %s, danceability = %s, duration_ms = %s, energy = %s, instrumentalness = %s, key = %s, liveness = %s, loudness = %s, mode = %s, speechiness = %s, tempo = %s, time_signature = %s, valence = %s WHERE spotify_uri = %s"
    data = (
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
        valence,
        uri
    )

    try:
        cursor.execute(SQL, data)
        conn.commit()
    except Exception as e:
        cursor.execute("ROLLBACK")
        conn.commit()
        print("Couldn't add song. %s" % e)

    print("Updated info of Spotify song %s" % uri)

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def fetch_song_general(song_name, artist_name):
    client_credentials_manager = SpotifyClientCredentials()
    spotify = spotipy.Spotify(
        client_credentials_manager=client_credentials_manager)

    query_artist = artist_name.split("&")[0].strip()
    query = "%s %s" % (song_name, query_artist)

    result = spotify.search(q=query, limit=20)

    if(len(result["tracks"]["items"]) > 0):
        song = result["tracks"]["items"][0]

        metadata = {
            "duration": song["duration_ms"],
            "release_date": song["album"]["release_date"],
            "popularity": song["popularity"],
            "song_name": song["name"],
            "artists": song["artists"],
            "uri": song["uri"],
        }

        artist_names = []
        for artist in song["artists"]:
            artist_names.append(artist["name"])

        print("Found: %s by %s (Id: %s)" % (
            metadata["song_name"], ", ".join(artist_names), metadata["uri"]))

        return metadata
    else:
        raise Exception("No match found for %s by %s" % (song_name, artist_name))


def fetch_spotify_audio_features(array):
    client_credentials_manager = SpotifyClientCredentials()
    spotify = spotipy.Spotify(
        client_credentials_manager=client_credentials_manager)

    audio_features = spotify.audio_features(array)

    return audio_features

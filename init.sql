CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE OR REPLACE FUNCTION update_timestamp_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    IF row(NEW.*) IS DISTINCT FROM row(OLD.*) THEN
      NEW.timestamp_modified = now();
      RETURN NEW;
    ELSE
      RETURN OLD;
    END IF;
END;
$$ language 'plpgsql';

CREATE TABLE IF NOT EXISTS Djs (
    id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    name varchar(255) NOT NULL,
    timestamp_added timestamp default current_timestamp,
    timestamp_modified timestamp
);
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_dj_timestamp_modified') THEN
        CREATE TRIGGER update_dj_timestamp_modified BEFORE UPDATE ON Djs FOR EACH ROW EXECUTE PROCEDURE update_timestamp_modified_column();
    END IF;
END
$$;

CREATE TABLE IF NOT EXISTS Artists (
    id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    name varchar(255) NOT NULL,
    timestamp_added timestamp default current_timestamp,
    timestamp_modified timestamp
);
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_artists_timestamp_modified') THEN
        CREATE TRIGGER update_artists_timestamp_modified BEFORE UPDATE ON Artists FOR EACH ROW EXECUTE PROCEDURE update_timestamp_modified_column();
    END IF;
END
$$;

CREATE TABLE IF NOT EXISTS Songs (
    id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    title varchar(255) NOT NULL,
    artist_id uuid NOT NULL,
    release_date date,
    duration int,
    spotify_uri varchar(255),
    timestamp_added timestamp default current_timestamp,
    timestamp_modified timestamp,
    FOREIGN KEY (artist_id) REFERENCES Artists(id)
);
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_songs_timestamp_modified') THEN
        CREATE TRIGGER update_songs_timestamp_modified BEFORE UPDATE ON Songs FOR EACH ROW EXECUTE PROCEDURE update_timestamp_modified_column();
    END IF;
END
$$;

CREATE TABLE IF NOT EXISTS Venues (
    id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    name varchar(255) NOT NULL,
    timestamp_added timestamp default current_timestamp,
    timestamp_modified timestamp
);
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_venues_timestamp_modified') THEN
        CREATE TRIGGER update_venues_timestamp_modified BEFORE UPDATE ON Venues FOR EACH ROW EXECUTE PROCEDURE update_timestamp_modified_column();
    END IF;
END
$$;

CREATE TABLE IF NOT EXISTS Occasions (
    id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    name varchar(255) NOT NULL,
    timestamp_added timestamp default current_timestamp,
    timestamp_modified timestamp
);
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_occasions_timestamp_modified') THEN
        CREATE TRIGGER update_occasions_timestamp_modified BEFORE UPDATE ON Occasions FOR EACH ROW EXECUTE PROCEDURE update_timestamp_modified_column();
    END IF;
END
$$;

CREATE TABLE IF NOT EXISTS Sets (
    id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    dj_id uuid NOT NULL,
    occasion_id uuid,
    venue_id uuid,
    recording_date date,
    source text UNIQUE,
    timestamp_added timestamp default current_timestamp,
    timestamp_modified timestamp,
    FOREIGN KEY (dj_id) REFERENCES Djs(id),
    FOREIGN KEY (occasion_id) REFERENCES Occasions(id),
    FOREIGN KEY (venue_id) REFERENCES Venues(id)
);
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_sets_timestamp_modified') THEN
        CREATE TRIGGER update_sets_timestamp_modified BEFORE UPDATE ON Sets FOR EACH ROW EXECUTE PROCEDURE update_timestamp_modified_column();
    END IF;
END
$$;

CREATE TABLE IF NOT EXISTS Transitions (
    song_from uuid NOT NULL,
    song_to uuid NOT NULL,
    set_id uuid NOT NULL,
    FOREIGN KEY (song_from) REFERENCES Songs(id),
    FOREIGN KEY (song_to) REFERENCES Songs(id),
    FOREIGN KEY (set_id) REFERENCES Sets(id),
    CONSTRAINT Transitions_UQ UNIQUE(song_from, song_to, set_id)
);

CREATE TABLE IF NOT EXISTS Tags (
    id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    name varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Song_Tags (
    song_id uuid,
    tag_id uuid,
    source text,
    FOREIGN KEY (song_id) REFERENCES Songs(id),
    FOREIGN KEY (tag_id) REFERENCES Tags(id),
    CONSTRAINT Song_Tags_UQ UNIQUE(song_id, tag_id, source)
);

CREATE TABLE IF NOT EXISTS Artist_Tags (
    artist_id uuid,
    tag_id uuid,
    source text,
    FOREIGN KEY (artist_id) REFERENCES Artists(id),
    FOREIGN KEY (tag_id) REFERENCES Tags(id),
    CONSTRAINT Artist_Id_UQ UNIQUE(artist_id, tag_id, source)
);

CREATE TABLE IF NOT EXISTS Spotify_Songs (
    spotify_uri varchar(255) PRIMARY KEY,
    song_id uuid NOT NULL UNIQUE,
    acousticness float,
    danceability float,
    duration_ms int,
    energy float,
    instrumentalness float,
    key int,
    mode int,
    liveness float,
    loudness float,
    speechiness float,
    tempo float,
    time_signature int,
    valence float,
    timestamp_added timestamp default current_timestamp,
    timestamp_modified timestamp,
    FOREIGN KEY (song_id) REFERENCES Songs(id)
);
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_spotify_songs_timestamp_modified') THEN
        CREATE TRIGGER update_spotify_songs_timestamp_modified BEFORE UPDATE ON Spotify_Songs FOR EACH ROW EXECUTE PROCEDURE update_timestamp_modified_column();
    END IF;
END
$$;

CREATE TABLE IF NOT EXISTS Spotify_Artists (
    spotify_uri varchar(255) PRIMARY KEY,
    artist_id uuid NOT NULL,
    followers int,
    popularity int,
    timestamp_added timestamp default current_timestamp,
    timestamp_modified timestamp,
    FOREIGN KEY (artist_id) REFERENCES Artists(id)
);
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_spotify_artists_timestamp_modified') THEN
        CREATE TRIGGER update_spotify_artists_timestamp_modified BEFORE UPDATE ON Spotify_Artists FOR EACH ROW EXECUTE PROCEDURE update_timestamp_modified_column();
    END IF;
END
$$;

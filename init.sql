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
CREATE TRIGGER update_dj_timestamp_modified BEFORE UPDATE ON Djs FOR EACH ROW EXECUTE PROCEDURE update_timestamp_modified_column();

CREATE TABLE IF NOT EXISTS Artists (
    id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    name varchar(255) NOT NULL,
    timestamp_added timestamp default current_timestamp,
    timestamp_modified timestamp
);
CREATE TRIGGER update_artists_timestamp_modified BEFORE UPDATE ON Artists FOR EACH ROW EXECUTE PROCEDURE update_timestamp_modified_column();

CREATE TABLE IF NOT EXISTS Songs (
    id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    title varchar(255) NOT NULL,
    artist_id uuid NOT NULL,
    release_date date,
    duration int,
    timestamp_added timestamp default current_timestamp,
    timestamp_modified timestamp,
    FOREIGN KEY (artist_id) REFERENCES Artists(id)
);
CREATE TRIGGER update_songs_timestamp_modified BEFORE UPDATE ON Songs FOR EACH ROW EXECUTE PROCEDURE update_timestamp_modified_column();

CREATE TABLE IF NOT EXISTS Venues (
    id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    name varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Occasions (
    id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    name varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Sets (
    id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    dj_id uuid NOT NULL,
    occasion_id uuid NOT NULL,
    venue_id uuid NOT NULL,
    recording_date date,
    source text,
    timestamp_added timestamp default current_timestamp,
    timestamp_modified timestamp,
    FOREIGN KEY (dj_id) REFERENCES Djs(id),
    FOREIGN KEY (occasion_id) REFERENCES Occasions(id),
    FOREIGN KEY (venue_id) REFERENCES Venues(id)
);
CREATE TRIGGER update_sets_timestamp_modified BEFORE UPDATE ON Sets FOR EACH ROW EXECUTE PROCEDURE update_timestamp_modified_column();

CREATE TABLE IF NOT EXISTS Transitions (
    song_from uuid NOT NULL,
    song_to uuid NOT NULL,
    set_id uuid NOT NULL,
    FOREIGN KEY (song_from) REFERENCES Songs(id),
    FOREIGN KEY (song_to) REFERENCES Songs(id),
    FOREIGN KEY (set_id) REFERENCES Sets(id),
    CONSTRAINT Transitions_UQ UNIQUE(song_from, song_to, set_id)
);

CREATE TABLE IF NOT EXISTS Songs_BPM (
    song_id uuid NOT NULL,
    bpm int NOT NULL,
    source text NOT NULL,
    FOREIGN KEY (song_id) REFERENCES Songs(id),
    CONSTRAINT Songs_BPM_UQ UNIQUE(song_id, bpm, source)
);

CREATE TABLE IF NOT EXISTS Songs_KEY (
    song_id uuid NOT NULL,
    key varchar(3) NOT NULL,
    source text NOT NULL,
    FOREIGN KEY (song_id) REFERENCES Songs(id),
    CONSTRAINT Songs_KEY_UQ UNIQUE(song_id, key, source)
);

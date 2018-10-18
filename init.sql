CREATE TABLE IF NOT EXISTS Djs (
    id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    name varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Artists (
    id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    name varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Songs (
    id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    title varchar(255) NOT NULL,
    artist_id uuid NOT NULL,
    release_date date,
    key varchar(3),
    duration int,
    FOREIGN KEY (artist_id) REFERENCES Artists(id)
);

CREATE TABLE IF NOT EXISTS Sets (
    id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    dj_id uuid NOT NULL,
    recording_date date,
    source text,
    FOREIGN KEY (dj_id) REFERENCES Djs(id)
);

CREATE TABLE IF NOT EXISTS Transitions (
    song_from uuid NOT NULL,
    song_to uuid NOT NULL,
    set_id uuid NOT NULL,
    FOREIGN KEY (song_from) REFERENCES Songs(id),
    FOREIGN KEY (song_to) REFERENCES Songs(id),
    FOREIGN KEY (set_id) REFERENCES Sets(id)
);

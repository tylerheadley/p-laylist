CREATE EXTENSION rum;

BEGIN;

--Users Table
CREATE TABLE users (
    id_user BIGSERIAL PRIMARY KEY,
    screen_name TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    password TEXT,
    spotify_access_token TEXT UNIQUE,
    spotify_refresh_token TEXT UNIQUE
);
CREATE INDEX idx_username_password ON users(screen_name, password);


--Artists Table
CREATE TABLE artists (
    id_artist BIGSERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    genre TEXT NOT NULL,
    description TEXT
);

-- Genres Table
CREATE TABLE genre (
    id_genre SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

-- Album Table
CREATE TABLE albums (
  	id_album SERIAL PRIMARY KEY,
    id_artist BIGINT NOT NULL,
    id_genre BIGINT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY (id_artist) REFERENCES artists(id_artist),
  	FOREIGN KEY (id_genre) REFERENCES genre(id_genre)
);

-- Songs Table
CREATE TABLE songs (
  	id_song SERIAL PRIMARY KEY,
  	id_album BIGINT NOT NULL,
    id_artist BIGINT NOT NULL,
    id_genre BIGINT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY (id_artist) REFERENCES artists(id_artist),
  	FOREIGN KEY (id_album) REFERENCES albums(id_album),
  	FOREIGN KEY (id_genre) REFERENCES genre(id_genre)
);

-- Playlists Table
CREATE TABLE playlists (
    id_playlist SERIAL PRIMARY KEY,
    id_user BIGINT,
    name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE
);

-- Songs in Playlists Table
CREATE TABLE playlist_songs (
    id_playlist BIGINT,
    id_song BIGINT,
    added_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (id_playlist, id_song),
    FOREIGN KEY (id_playlist) REFERENCES playlists(id_playlist) ON DELETE CASCADE,
    FOREIGN KEY (id_song) REFERENCES songs(id_song) ON DELETE CASCADE
);

-- Songs Listened Table
CREATE TABLE songs_listened (
    id_user BIGINT NOT NULL,
    id_song BIGINT NOT NULL,
    listened_at TIMESTAMPTZ NOT NULL,
    FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE,
    FOREIGN KEY (id_song) REFERENCES songs(id_song) ON DELETE CASCADE
);

-- Friends Table
CREATE TABLE friends {
    id_user BIGINT NOT NULL,
    id_friend BIGINT NOT NULL,
    added_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_user, id_friend),
    FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE,
    FOREIGN KEY (id_friend) REFERENCES users(id_user) ON DELETE CASCADE,
}

COMMIT;
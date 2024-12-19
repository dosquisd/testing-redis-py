CREATE TABLE IF NOT EXISTS authors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    nacionality TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    genre TEXT NOT NULL,
    id_author INTEGER NOT NULL,

    FOREIGN KEY (id_author) REFERENCES authors(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

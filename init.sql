CREATE TABLE users (
    id INTEGER NOT NULL,
    first_name TEXT,
    last_name TEXT,
    full_name, TEXT,
    PRIMARY KEY(id)
);

CREATE TABLE threads (
    id INTEGER NOT NULL,
    name TEXT,
    type TEXT,
    PRIMARY KEY(id)
);

CREATE TABLE participants (
    id INTEGER NOT NULL,
    thread_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(thread_id) REFERENCES threads(id),
    FOREIGN KEY(user_id) REFERENCES users(id),
    PRIMARY KEY(id)
);

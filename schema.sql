CREATE TABLE dangers (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	desc TEXT NOT NULL,
	level TEXT NOT NULL,
	lat float NOT NULL,
	lng float NOT NULL,
        username text not null
);


CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
	hash TEXT NOT NULL
);

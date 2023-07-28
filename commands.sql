CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL);
INSERT INTO users (username, hash) VALUES ('user1', 'pass1');
SELECT * FROM users;

CREATE TABLE cats (id_cat INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, age TEXT NOT NULL, gender TEXT NOT NULL, location TEXT NOT NULL, description TEXT NOT NULL, photo_path TEXT NOT NULL, user_id INTEGER, FOREIGN KEY (user_id) REFERENCES users(id));

name, age, gender, location, description, photo_path
/* # source link: https://flask.palletsprojects.com/en/2.0.x/tutorial/database/
#################################################
this file is to create a schema for database */
/* This will check the following tables existance or not. */
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

/*This will create user table with columns: id, username, and password */
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

/* This will create post table with columns: id, author_id(set foreign key with user), created (date), title, body*/
CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
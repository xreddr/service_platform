PRAGMA foreign_keys = off;

BEGIN TRANSACTION;

DROP TABLE IF EXISTS recipe;
CREATE TABLE IF NOT EXISTS recipe (
    id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL UNIQUE,
    recipe TEXT NOT NULL UNIQUE,
    keywords TEXT,
    PRIMARY KEY(id AUTOINCREMENT),
    FOREIGN KEY(user_id) REFERENCES user(id)
);
DROP TABLE IF EXISTS cookbook_user_keyword;
CREATE TABLE IF NOT EXISTS keyword (
    id INTEGER NOT NULL,
    user_id INTEGER NOT NULL UNIQUE,
    keyword JSON NOT NULL,
    PRIMARY KEY(id AUTOINCREMENT),
    FOREIGN KEY(user_id) REFERENCES user(id)
);
DROP TABLE IF EXISTS recipe_keyword;
CREATE TABLE IF NOT EXISTS recipe_keyword (
    recipe_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    keyword text NOT NULL,
    FOREIGN KEY(recipe_id) REFERENCES recipe(id),
    FOREIGN KEY(user_id) REFERENCES user(id)
);

COMMIT TRANSACTION;

PRAGMA foreign_keys = on;
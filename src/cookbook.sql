PRAGMA foreign_keys = off;

BEGIN TRANSACTION;

DROP TABLE IF EXISTS user_recipe;
CREATE TABLE IF NOT EXISTS user_recipe (
    user_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(recipe_id) REFERENCES recipte(id)
);
DROP TABLE IF EXISTS recipe;
CREATE TABLE IF NOT EXISTS recipe (
    id INTEGER NOT NULL,
    title TEXT NOT NULL UNIQUE,
    recipe TEXT NOT NULL UNIQUE,
    keywords TEXT,
    PRIMARY KEY(id AUTOINCREMENT)
);
DROP TABLE IF EXISTS keyword;
CREATE TABLE IF NOT EXISTS keyword (
    id INTEGER NOT NULL,
    keyword TEXT NOT NULL UNIQUE,
    PRIMARY KEY(id AUTOINCREMENT)
);
DROP TABLE IF EXISTS recipe_keyword;
CREATE TABLE IF NOT EXISTS recipe_keyword (
    recipe_id INTEGER NOT NULL,
    keyword_id INTEGER NOT NULL,
    FOREIGN KEY(recipe_id) REFERENCES recipe(id),
    FOREIGN KEY(keyword_id) REFERENCES keyword(id)
);

COMMIT TRANSACTION;

PRAGMA foreign_keys = on;
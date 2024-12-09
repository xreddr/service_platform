-- Add category table.
-- Add recipe_category table.

PRAGMA foreign_keys = off;

BEGIN TRANSACTION;

DROP TABLE IF EXISTS cookbook_category;
CREATE TABLE IF NOT EXISTS cookbook_category (
    id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    PRIMARY KEY(id AUTOINCREMENT),
    FOREIGN KEY(user_id) REFERENCES user(id)
);

DROP TABLE IF EXISTS recipe_category;
CREATE TABLE IF NOT EXISTS recipe_category (
    recipe_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY(recipe_id, category_id)
);

COMMIT TRANSACTION;

PRAGMA foreign_keys = on;
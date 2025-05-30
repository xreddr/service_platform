PRAGMA foreign_keys = off;

BEGIN TRANSACTION;

DROP TABLE IF EXISTS recipe_date;
CREATE TABLE IF NOT EXISTS recipe_date (
    id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    PRIMARY KEY(id AUTOINCREMENT),
    FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY(recipe_id) REFERENCES recipe(id) ON DELETE CASCADE
);

COMMIT TRANSACTION;

PRAGMA foreign_keys = on;
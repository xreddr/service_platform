PRAGMA foreign_keys = off;

BEGIN TRANSACTION;

ALTER TABLE cookbook_category RENAME TO cookbook_category_old;
DROP TABLE IF EXISTS cookbook_category;
CREATE TABLE IF NOT EXISTS cookbook_category (
    id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    PRIMARY KEY(id AUTOINCREMENT),
    FOREIGN KEY(user_id) REFERENCES user(id)
);
INSERT INTO cookbook_category (user_id, name) SELECT user_id, name FROM cookbook_category_old;

ALTER TABLE recipe_category RENAME TO recipe_category_old;
DROP TABLE IF EXISTS recipe_category;
CREATE TABLE IF NOT EXISTS recipe_category (
    recipe_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY(recipe_id, category_id)
);
INSERT INTO recipe_category (recipe_id, category_id) SELECT recipe_id, category_id FROM recipe_category_old;

COMMIT TRANSACTION;

PRAGMA foreign_keys = on;
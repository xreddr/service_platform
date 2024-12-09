-- Remove cookbook_category table.
-- Remove recipe_category table.

PRAGMA foreign_keys = off;

BEGIN TRANSACTION;

DROP TABLE IF EXISTS cookbook_category;

DROP TABLE IF EXISTS recipe_category;

COMMIT TRANSACTION;

PRAGMA foreign_keys = off;

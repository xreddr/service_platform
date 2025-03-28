PRAGMA foregin_keys = off;

BEGIN TRANSACTION;

DROP TABLE IF EXISTS recipe_date;

COMMIT TRANSACTION;

PRAMA foregin_keys = on;
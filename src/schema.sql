BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "user" (
    "id" INTEGER NOT NULL,
    "username" TEXT NOT NULL UNIQUE,
    "password" TEXT NOT NULL,
     PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "post" (
    "id" INTEGER NOT NULL,
    "date" DATE NOT NULL,
    "body" TEXT NOT NULL,
    "image" TEXT
    "author" TEXT NOT NULL,
    "type" TEXT,
    PRIMARY KEY("id" AUTOINCREMENT),
    FOREIGN KEY("author") REFERENCES "user"("id")
);
CREATE TABLE IF NOT EXISTS "comment" (
    "id" INTEGER NOT NULL,
    "date" DATE NOT NULL,
    "body" TEXT NOT NULL,
    "author" TEXT NOT NULL,
    "post" INTEGER NOT NULL,
    PRIMARY KEY("id" AUTOINCREMENT),
    FOREIGN KEY("post") REFERENCES "post"("id")
);

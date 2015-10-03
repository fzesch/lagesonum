ALTER TABLE numbers RENAME TO old_numbers;
ALTER TABLE places RENAME TO old_places;
ALTER TABLE users RENAME TO old_users;

DELETE FROM old_numbers WHERE number IN ('A123', '2015', 'A00000');
UPDATE old_numbers SET number = UPPER(number);

CREATE TABLE "user" ("id" INTEGER NOT NULL PRIMARY KEY, "username" VARCHAR(10) NOT NULL, "password" VARCHAR(20) NOT NULL, "is_admin" SMALLINT NOT NULL);
CREATE UNIQUE INDEX "user_username" ON "user" ("username");
CREATE TABLE "place" ("id" INTEGER NOT NULL PRIMARY KEY, "valregexp" VARCHAR(99) NOT NULL, "place" VARCHAR(20) NOT NULL, "min_length" INTEGER NOT NULL, "max_length" INTEGER NOT NULL);
CREATE TABLE "number" ("id" INTEGER NOT NULL PRIMARY KEY, "number" VARCHAR(30) NOT NULL, "time" DATETIME NOT NULL, "user_id" INTEGER, "place_id" INTEGER NOT NULL, "fingerprint" VARCHAR(32) NOT NULL, FOREIGN KEY ("user_id") REFERENCES "user" ("id"), FOREIGN KEY ("place_id") REFERENCES "place" ("id"));
CREATE INDEX "number_place_id" ON "number" ("place_id");
CREATE INDEX "number_user_id" ON "number" ("user_id");
CREATE UNIQUE INDEX "number_number_fingerprint" ON "number" ("number", "fingerprint");

INSERT INTO place VALUES(1, '\b[a-z0-9]{4}\b', 'LAGESO', 0, 10);
INSERT INTO number (number, time, place_id, fingerprint) SELECT number, time, 1, fingerprint FROM old_numbers;

DROP TABLE old_numbers;
DROP TABLE old_users;
DROP TABLE old_places;

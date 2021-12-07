/* vittuilutietokannan rakenne (ja perustaminen) */

-- tietokantainstanssi: vittuilu-db

CREATE DATABASE vittuilu;

CREATE TABLE low (id SERIAL PRIMARY KEY, nimi varchar(255) NOT NULL, email varchar(255) NOT NULL, paikkakunta varchar(255) NOT NULL);
CREATE TABLE medium (id SERIAL PRIMARY KEY, nimi varchar(255) NOT NULL, email varchar(255) NOT NULL, paikkakunta varchar(255) NOT NULL);
CREATE TABLE high (id SERIAL PRIMARY KEY, nimi varchar(255) NOT NULL, email varchar(255) NOT NULL, paikkakunta varchar(255) NOT NULL);
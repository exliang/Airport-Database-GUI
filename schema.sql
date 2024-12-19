-- schema.sql
--
-- ICS 33 Spring 2024
-- Project 2: Learning to Fly
--
-- YOU WILL NOT NEED TO MODIFY THIS FILE OR EXECUTE IT IN ANY WAY.  It is
-- provided only to show you the structure of the database that's already
-- in "airport.db".
--
-- The data dictionary available at the following link describes the meanings
-- of the corresponding columns in the original data from which "airport.db"
-- was created.
--
-- https://ourairports.com/help/data-dictionary.html


CREATE TABLE continent (
    continent_id INTEGER NOT NULL PRIMARY KEY,
    continent_code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL
) STRICT;


CREATE TABLE country (
    country_id INTEGER NOT NULL PRIMARY KEY,
    country_code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    continent_id INTEGER NOT NULL,
    wikipedia_link TEXT NOT NULL,
    keywords TEXT NULL,
    FOREIGN KEY (continent_id) REFERENCES continent (continent_id)
) STRICT;


CREATE TABLE region (
    region_id INTEGER NOT NULL PRIMARY KEY,
    region_code TEXT NOT NULL UNIQUE,
    local_code TEXT NOT NULL,
    name TEXT NOT NULL,
    continent_id INTEGER NOT NULL,
    country_id INTEGER NOT NULL,
    wikipedia_link TEXT NULL,
    keywords TEXT NULL,
    FOREIGN KEY (continent_id) REFERENCES continent (continent_id),
    FOREIGN KEY (country_id) REFERENCES country (country_id)
) STRICT;


CREATE TABLE airport (
    airport_id INTEGER NOT NULL PRIMARY KEY,
    airport_ident TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,
    name TEXT NOT NULL,
    latitude_deg REAL NOT NULL,
    longitude_deg REAL NOT NULL,
    elevation_ft INTEGER NULL,
    continent_id TEXT NOT NULL,
    country_id INTEGER NOT NULL,
    region_id INTEGER NOT NULL,
    municipality TEXT NULL,
    scheduled_service INTEGER NOT NULL,
    gps_code TEXT NULL,
    iata_code TEXT NULL,
    local_code TEXT NULL,
    home_link TEXT NULL,
    wikipedia_link TEXT NULL,
    keywords TEXT NULL,
    FOREIGN KEY (continent_id) REFERENCES continent (continent_id),
    FOREIGN KEY (country_id) REFERENCES country (country_id),
    FOREIGN KEY (region_id) REFERENCES region (region_id)
) STRICT;


CREATE TABLE airport_frequency (
    airport_frequency_id INTEGER NOT NULL PRIMARY KEY,
    airport_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    description TEXT NULL,
    frequency_mhz REAL NOT NULL,
    FOREIGN KEY (airport_id) REFERENCES airport (airport_id)
) STRICT;


CREATE TABLE runway (
    runway_id INTEGER NOT NULL PRIMARY KEY,
    airport_id INTEGER NOT NULL,
    length_ft INTEGER NULL,
    width_ft INTEGER NULL,
    surface TEXT NULL,
    lighted INTEGER NOT NULL,
    closed INTEGER NOT NULL,
    le_ident TEXT NULL,
    le_latitude_deg REAL NULL,
    le_longitude_deg REAL NULL,
    le_elevation_ft INTEGER NULL,
    le_heading_deg REAL NULL,
    le_displaced_threshold_ft INTEGER NULL,
    he_ident TEXT NULL,
    he_latitude_deg REAL NULL,
    he_longitude_deg REAL NULL,
    he_elevation_ft INTEGER NULL,
    he_heading_deg REAL NULL,
    he_displaced_threshold_ft INTEGER NULL,
    FOREIGN KEY (airport_id) REFERENCES airport (airport_id)
) STRICT;


CREATE TABLE navigation_aid (
    navigation_aid_id INTEGER NOT NULL,
    filename TEXT NOT NULL,
    ident TEXT NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    frequency_khz INTEGER NOT NULL,
    latitude_deg REAL NOT NULL,
    longitude_deg REAL NOT NULL,
    elevation_ft INTEGER NULL,
    iso_country TEXT NOT NULL,
    dme_frequency_khz INTEGER NULL,
    dme_channel TEXT NULL,
    dme_latitude_deg REAL NULL,
    dme_longitude_deg REAL NULL,
    dme_elevation_ft INTEGER NULL,
    adjusted_variation_deg REAL NULL,
    magnetic_variation_deg REAL NULL,
    usage_type TEXT NULL,
    power TEXT NULL,
    airport_id INTEGER NULL,
    FOREIGN KEY (airport_id) REFERENCES airport (airport_id)
) STRICT;

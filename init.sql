CREATE DATABASE earthquake_db;
GRANT ALL PRIVILEGES ON DATABASE "earthquake_db" to saeed;
\c earthquake_db;
create table earthquakes (
        id          BIGSERIAL PRIMARY KEY,
		mag         numeric,
        mag_type    varchar,
        place       varchar(500),
        time        timestamp without time zone,
        title       varchar
);
create extension postgis;
SELECT AddGeometryColumn ('earthquakes', 'geom', 4326, 'POINT', 3);

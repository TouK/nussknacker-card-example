#!/bin/bash
set -e

echo "COUNTRY	POSTAL_CODE	NAME	N1	C1	N2	C2	N3	C3	LATITUDE	LONGITUDE	ACCURACY" > /tmp/codes.tsv
gunzip -c /tmp/PL.txt.gz | sort -u >> /tmp/codes.tsv

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE TABLE ADDRESSES(
     COUNTRY        TEXT    NOT NULL,
     POSTAL_CODE    TEXT    NOT NULL,
     NAME           TEXT    NOT NULL,
     N1             TEXT,
     C1             TEXT,
     N2             TEXT,
     C2             TEXT,
     N3             TEXT,
     C3             TEXT,
     LATITUDE       numeric NOT NULL,
     LONGITUDE      numeric NOT NULL,
     ACCURACY       TEXT    NOT NULL);
  CREATE INDEX codes on ADDRESSES (POSTAL_CODE);
  COPY ADDRESSES
  FROM '/tmp/codes.tsv'
  DELIMITER E'\t'
  CSV HEADER;
EOSQL

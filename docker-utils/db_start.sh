#!/usr/bin/env bash


set -e
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
	CREATE USER docker;
	CREATE DATABASE sias;
	GRANT ALL PRIVILEGES ON DATABASE docker TO docker;
EOSQL
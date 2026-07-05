-- Run after PostgreSQL starts (mounted into /docker-entrypoint-initdb.d)
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

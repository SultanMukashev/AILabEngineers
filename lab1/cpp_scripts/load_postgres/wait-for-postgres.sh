#!/bin/sh
set -e

echo "Waiting for Postgres to be ready..."

# Make sure pg_isready is available by installing postgresql-client in Dockerfile
until pg_isready -h postgres -p 5432 -U user; do
  sleep 1
done

echo "Postgres is ready! Starting the app..."
exec ./app
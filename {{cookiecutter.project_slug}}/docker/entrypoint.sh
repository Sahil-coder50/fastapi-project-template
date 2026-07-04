#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."

while ! nc -z postgres 5432; do
    sleep 1
done

echo "PostgreSQL is available."

if [ "$RUN_MIGRATIONS" = "1" ]; then
    echo "Running Alembic migrations..."
    alembic upgrade head
fi

echo "Starting FastAPI..."

exec "$@"
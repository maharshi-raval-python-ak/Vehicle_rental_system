#!/bin/sh
echo "Database is ready! Running migrations..."
alembic upgrade head

echo "Starting FastAPI..."
exec "$@"

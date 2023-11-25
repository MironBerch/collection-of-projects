#!/bin/sh

while ! nc -z $ADMIN_POSTGRES_HOST $ADMIN_POSTGRES_PORT; do
  sleep 0.1
done

echo "Postgres did run"

# Run the main container process
exec "$@"

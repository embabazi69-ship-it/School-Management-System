
#!/bin/sh
# wait-for-db.sh - simple wait for postgres to be ready
set -e
host="$1"
shift
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "$POSTGRES_USER" -c '\q' 2>/dev/null; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
>&2 echo "Postgres is up - executing command"
exec "$@"

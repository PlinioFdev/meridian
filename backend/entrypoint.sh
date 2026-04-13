#!/bin/sh

echo "Waiting for database..."
while ! python -c "
import psycopg2, os
psycopg2.connect(
    dbname=os.environ['POSTGRES_DB'],
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    host=os.environ['POSTGRES_HOST'],
    port=os.environ['POSTGRES_PORT']
)
" 2>/dev/null; do
  sleep 1
done
echo "Database ready."

python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear 2>/dev/null || true

exec "$@"

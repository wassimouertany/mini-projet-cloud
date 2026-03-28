#!/bin/sh

echo "Waiting for PostgreSQL..."

while ! nc -z db 5432; do
  sleep 1
done

echo "PostgreSQL is ready!"

echo "Creating tables..."
python -c "
from app import app
from models import db
with app.app_context():
    db.create_all()
    print('Tables created!')
"

echo "Starting Flask..."
exec python app.py
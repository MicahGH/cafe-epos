#!/usr/bin/env bash
set -e

if ! grep -q "^API_KEY=" .env; then
    echo 'Error: API_KEY is not set in .env! Please add the line: API_KEY="demo"'
    exit 1
fi

echo "Starting PostgreSQL container..."
docker rm -f pg_cafe_db_container
docker compose up -d --remove-orphans

echo "Installing dependencies..."
poetry install --no-root

echo "Adding dotenv plugin (if not installed)..."
poetry self add poetry-dotenv-plugin || true

echo "Running migrations..."
poetry run python manage.py makemigrations
poetry run python manage.py migrate

echo "Seeding menu items..."
poetry run python manage.py seed_menu_items

echo "All done! You can now run the server with:"
echo "poetry run python manage.py runserver"

#!/bin/bash

echo "🚀 Deploying Reader's Hub API..."

# Pull latest changes
git pull origin main

# Install/update dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart application server (example for Gunicorn)
sudo systemctl restart gunicorn

# Restart Nginx
sudo systemctl restart nginx

echo "✅ Deployment complete!"
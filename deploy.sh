#!/bin/bash

echo "🚀 Starting deployment..."

# Step 1: Check .env
if [ ! -f .env ]; then
  echo "❌ .env file not found!"
  exit 1
fi
echo "✅ .env file found"

# Step 2: Activate venv
if [ -d "book_review_env" ]; then
  source book_review_env/bin/activate
  echo "✅ Virtual environment activated"
fi

# Step 3: Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Step 4: Django check
echo "🔌 Checking Django..."
python manage.py check || exit 1

# Step 5: Migrations
echo "🛠 Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Step 6: Collect static
echo "📁 Collecting static..."
python manage.py collectstatic --noinput

# Step 7: Optional superuser
read -p "Create superuser? (y/n): " choice
if [ "$choice" = "y" ]; then
  python manage.py createsuperuser
fi

# Step 8: Run server
echo "🔥 Starting server..."
python manage.py runserver
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys
from dotenv import load_dotenv

def main():
    """Run administrative tasks."""
    try:
        # Load .env
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        load_dotenv(os.path.join(base_dir, ".env"))

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "book_review_project.settings")
        from django.core.management import execute_from_command_line

        # Check for DB connection before running commands
        if "runserver" in sys.argv or "migrate" in sys.argv:
            from django.db import connections
            from django.db.utils import OperationalError
            db_conn = connections['default']
            try:
                db_conn.ensure_connection()
                print("✅ Database connection successful!")
            except OperationalError:
                print("❌ Database connection failed. Check your .env or DATABASE_URL.")
                sys.exit(1)

        execute_from_command_line(sys.argv)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
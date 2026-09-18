#!/bin/bash

# Initialize database if it doesn't exist or is empty
if [ ! -f /app/instance/evaluations.db ] || [ ! -s /app/instance/evaluations.db ]; then
    echo "Initializing database..."
    python init_db.py
    echo "Importing data..."
    python import_data.py
else
    # Check if tables exist
    TABLE_COUNT=$(python -c "
import sqlite3
conn = sqlite3.connect('/app/instance/evaluations.db')
cursor = conn.cursor()
cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table' AND name='manuscript'\")
result = cursor.fetchone()
conn.close()
print('1' if result else '0')
")
    if [ "$TABLE_COUNT" = "0" ]; then
        echo "Database tables missing, reinitializing..."
        python init_db.py
        python import_data.py
    else
        echo "Database already initialized."
    fi
fi

# Start the application
echo "Starting ENIP Human Evaluation Web App..."
exec gunicorn --bind 0.0.0.0:8080 --workers 4 app:app

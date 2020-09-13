#!/bin/bash

#collect static files
echo "Collect static files"
python3 van_oak/manage.py collectstatic --noinput

# Apply database migrations
echo "Apply db migrations"
python3 van_oak/manage.py migrate
python manage.py initadmin
python3 van_oak/manage.py createsuperuser
# Start server
echo "Starting server"
python van_oak/manage.py runserver 0.0.0.0:8000

#!/usr/bin/env bash
# install dependencies
pip install -r requirements.txt

# collect static files
python manage.py collectstatic --noinput

# apply migrations (only for SQLite or minimal database use)
python manage.py migrate

web: gunicorn taskmanager.wsgi --log-file -
web: python manage.py migrate && gunicorn app.wsgi
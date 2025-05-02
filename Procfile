web: uvicorn taskmanager:app --host 0.0.0.0 --port $PORT
web: gunicorn taskmanager.wsgi --log-file -
web: python manage.py migrate && gunicorn app.wsgi

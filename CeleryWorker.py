import os

os.system('celery worker -A FlaskApp.celery -E')

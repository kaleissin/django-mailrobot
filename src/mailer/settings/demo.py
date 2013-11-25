from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'mailer.sqlite3',                      # Or path to database file if using sqlite3.
    }
}

SECRET_KEY = 'na2Tei0FoChe3ooloh5Yaec0ji7Aipho'

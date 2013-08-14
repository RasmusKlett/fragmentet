from settings_base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'fragmentet',            # Or path to database file if using sqlite3.
        'USER': 'root',                  # Not used with sqlite3.
        'PASSWORD': 'root',              # Not used with sqlite3.
        'HOST': '',             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                  # Set to empty string for default. Not used with sqlite3.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en//ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Make this unique, and don't share it with anybody.
SECRET_KEY = '_rv8oii0cw^9oi4oo%zxglpk^2grc59x*77m6z=3$48k7=yh=w'

from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SECRET_KEY = 'na2Tei0FoChe3ooloh5Yaec0ji7Aipho'

SOUTH_TESTS_MIGRATE = False
SKIP_SOUTH_TESTS = True

if django.VERSION[:2] < (1, 6):
    TEST_RUNNER = 'discover_runner.DiscoverRunner'
    TEST_DISCOVER_ROOT = SITE_ROOT
    INSTALLED_APPS += ('discover_runner',)
TEST_DISCOVER_TOP_LEVEL = SITE_ROOT
TEST_DISCOVER_PATTERN = "*"

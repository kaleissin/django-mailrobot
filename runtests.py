import sys

from django.conf import settings

sys.path.append('./src')

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'mailrobot',
    )
)

if __name__ == '__main__':
    # MUST be imported *after* settings.configure() has run!
    from django.test.simple import DjangoTestSuiteRunner
    test_runner = DjangoTestSuiteRunner(verbosity=1)
    failures = test_runner.run_tests(['mailrobot', ])
    if failures:
        sys.exit(failures)

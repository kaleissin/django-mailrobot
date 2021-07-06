DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SECRET_KEY = 'na2Tei0FoChe3ooloh5Yaec0ji7Aipho'

INSTALLED_APPS=(
    'mailrobot',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': False,
        'OPTIONS': {
            'debug': DEBUG,
        },
    },
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

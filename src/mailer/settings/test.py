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

# To shut up a warning in Django 1.7
MIDDLEWARE_CLASSES=()

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': False,
        'OPTIONS': {
            'debug': DEBUG,
        },
    },
]

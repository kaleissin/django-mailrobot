import sys, os, os.path

_HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_HOME)
os.environ["DJANGO_SETTINGS_MODULE"] = "mailer.settings.demo"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

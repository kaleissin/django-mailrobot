.. index:: ! installation
    pair: installation; INSTALLED_APPS
    pair: installation; pip
    pair: installation; migrate
    pair: installation; syncdb

Installation
============

1. Install library, for instance with pip::

    pip install django-mailrobot

2. Add library to your INSTALLED_APPS in your settings::

    INSTALLED_APPS += ['mailrobot']

3. Add the tables.

   Prior to django 1.7::

        $ ./manage.py syncdb

   With South::

        $ ./manage.py schemamigration --initial mailrobot
        $ ./manage.py migrate mailrobot

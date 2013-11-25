================
django-mailrobot
================

Stores and sends canned email responses.

Ever had to change the signature or add a recipient to N hardcoded emails
spread all throughout your code? Hardcode no more! Use mailrobot instead.

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

Usage
=====

Add mails and addresses through the django admin.

In code
-------

Fetch a mail-template::

    template = Mail.objects.get(name='hello-world').

Fill it::

    mail = template.make_message(
        sender='Yep <overridden-from@example.com'>,
        recipients=('extra1@example.com', u'Blåbærsyltetøy <extra2@example.com>'),
        context={'world': 'Mailrobot'}
    )

Have a look::

    print mail.message

Send it::

    mail.send()

Niceties
========

In case you need to send an email somewhere else for
testing/debugging, clone an existing email in the admin:

1. Select it
2. Choose "Clone selected mails" in the action list
3. Hit "Go"

The clone will share everything with its original except the name,
which will be suffixed with a timestamp.

Edit the name of the clone to what you need, change recipients,
CCs, BCCs. Then, where you send the mail from, choose the clone if

:Version: 0.2
settings.DEBUG is True.

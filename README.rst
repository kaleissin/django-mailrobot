================
django-mailrobot
================

Stores and sends canned email responses.

Ever had to change the signature or add a recipient to N hardcoded emails
spread all throughout your code? Hardcode no more! Use mailrobot instead.

Depends on Django, with a version between 1.11 and 2.2, inclusive.

Installation
============

1. Install the library, for instance with pip::

    pip install django-mailrobot

2. Add the library to your INSTALLED_APPS of an exiting project::

    INSTALLED_APPS += ['mailrobot']

3. Add the tables to the existing project.

   ::

        $ ./manage.py migrate

Demo
====

Copy the entire django-mailrobot directory somewhere, set up and enter a
virtualenv, then provided you are on some Un*x::

    make demo

This'll create a demo-user "demo" with the password "demo".

The demo should now be running on http://127.0.0.1/

Tests
=====

To run the tests, first install the testing-requirements::

    pip install -r requirements/test.txt

then run the tests with::

    make test APP=mailrobot

Development
===========

Install the dev-requirements with::

    pip install -r requirements/test.txt

This'll give you ipython for a prettier shell-experience, but more importantly
it'll install pre-commit. Pre-commit will check for syntax errors and merge
conflicts, and fix trailing whitespaces and mixed line-endings for you.

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
settings.DEBUG is True.

:Version: 0.7.0

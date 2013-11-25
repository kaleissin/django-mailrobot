.. index:: ! usage

Usage
=====

Add mails and addresses through the django admin.

In code
-------

.. index::
    pair: usage; fetch template
    pair: template; fetch

Fetch a mail-template::

    template = Mail.objects.get(name='hello-world').

.. index::
    pair: usage; fill template
    pair: template; fill

Fill it::

    mail = template.make_message(
        sender='Yep <overridden-from@example.com'>,
        recipients=('extra1@example.com', u'Blåbærsyltetøy <extra2@example.com>'),
        context={'world': 'Mailrobot'}
    )

.. index::
    pair: usage; examine generated email
    pair: message; examine

Have a look::

    print mail.message

.. index::
    pair: usage; send email
    pair: message; send 

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

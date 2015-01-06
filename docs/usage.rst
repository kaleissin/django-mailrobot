.. index:: ! usage

Usage
=====

Add mails and addresses through the django admin.

Address
-------

Contains email-addresses.

::

    addr1 = Address.objects.create(
        address='ceo@example.com',
        comment='Bossman'
    )

This'll print as ``Bossman <ceo@example.com>``. The comment is optional::

    addr2 = Address.objects.create(
        address='ceo@example.com'
    )

This'll print as ``ceo@example.com``.

Signature
---------

Contains signatures.

::

    sig1 = Signature.objects.create(
        name='hello-world',
        sig="Test-system 'R us"
    )

A good ``name`` makes the ``Signature`` easier to find in the admin.

The sig is a django template stored in a text-field and thus of unlimited
length, but please do keep it to four lines or less!

MailBody
--------

Contains the subject and (plaintext) body.

::

    mb = MailBody.objects.create(
        name='hello-world',
        subject='Hello, {{ world|default:"World" }}!',
        body="""This is a test of the email-system."""
    )

The ``name`` should be url-safe and is primarily used to find it again in the
admin. A slugified version of the ``subject`` will work fine.

Both ``subject`` and ``body`` are django templates.


Mail
----

Combines a MailBody with an optional Signature and optional addresses.

::

    m = Mail.objects.create(
        name='hello-world',
        signature=sig1,
        content=mb,
        sender=addr1,
        reply_to=addr2,
    )

The ``name`` here is what you use to look up the mail in your code.

The ``sender`` and ``reply_to`` are otional and can be overridden later.

The recipients are ``Address`` querysets::

    m.recipients = addresses_for_the_To_field
    m.ccs = addresses_for_the_Cc_field
    m.bccs = addresses_for_the_Bcc_field

When saved on the ``Mail`` like this they cannot be overriden later, only
appended to.

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

    sender = 'Yep <overridden-from@example.com'>
    recipients = ('extra1@example.com', u'Blåbærsyltetøy <extra2@example.com>')
    context = {'world': 'Mailrobot'}

    mail = template.make_message(
        sender=sender,
        recipients=recipients,
        context=context
    )

The ``sender`` here is **a string** and overrides whatever is already is stored
in the mail. Notice that the ``recipients`` is an **iterable of strings**.

If you want to use one or more ``Address`` instead you need to convert the
queryset to an iterable of strings, for instance via::

    recipients = [str(address) for address in Address.objects.all()]

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

Edit the name of the clone to what you need, change recipients, CCs, BCCs.
Then, where you send the mail from, choose the clone if ``DEBUG`` is ``True``.

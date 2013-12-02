import time
from copy import deepcopy
import warnings

from django.db import models
from django.template import Context, Template
from django.core.mail import EmailMessage

def _render_from_string(templatestring, context=None):
    if context is None:
        context = {}
    template = Template(templatestring)
    return template.render(Context(context))

class MailrobotError(ValueError):
    pass

class MailrobotNoSenderError(MailrobotError):
    pass

class MailrobotNoRecipientsError(MailrobotError):
    pass

class NameManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

class AbstractNamedModel(models.Model):
    NAME_MAX_LENGTH = 40
    name = models.SlugField(max_length=NAME_MAX_LENGTH, unique=True)

    objects = NameManager()

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return self.name

    def clone(self):
        "Clone and return a Named model"

        newself = deepcopy(self)
        newself.pk = None
        newself.name = '%s-%.0f' % (self.name, time.time())
        newself.save(force_insert=True)
        return newself

class AddressManager(models.Manager):
    def get_by_natural_key(self, address):
        return self.get(address=address)

class Address(models.Model):
    address = models.EmailField(unique=True)
    comment = models.CharField(max_length=66, blank=True, null=True)

    objects = AddressManager()

    class Meta:
        verbose_name_plural = 'addresses'

    def __unicode__(self):
        if self.comment:
            return u'%s <%s>' % (self.comment, self.address)
        return self.address

    def natural_key(self):
        return self.address

class Signature(AbstractNamedModel):
    """Email signature

    No validation as to size.
    """

    sig = models.TextField()

    def attach(self, context=None):
        """
        The signature is attached like so:

        ::

                the final line of content


                --
                signature
        """

        signature = _render_from_string(self.sig, context)
        if signature:
            return u'\r\n\r\n\r\n-- \r\n%s' % signature
        return u''

class MailBody(AbstractNamedModel):
    "Subject and bodytext of the email"

    subject = models.CharField(max_length=66)
    body = models.TextField()

    class Meta:
        verbose_name_plural = 'mailbodies'

class Mail(AbstractNamedModel):
    """Canned Mail with default sender, Reply-To and recipients

    Verifies that there is a sender and at least one recipient.
    """

    KEYFIELD_DEFAULTS = {
        'null': True,
        'blank': True,
    }

    content = models.ForeignKey(MailBody, on_delete=models.CASCADE, related_name='mail')
    signature = models.ForeignKey(Signature, related_name='mail', **KEYFIELD_DEFAULTS)
    sender = models.ForeignKey(Address, related_name='sender', **KEYFIELD_DEFAULTS)
    recipients = models.ManyToManyField(Address, related_name='recipients', **KEYFIELD_DEFAULTS)
    ccs = models.ManyToManyField(Address, related_name='cc', **KEYFIELD_DEFAULTS)
    bccs = models.ManyToManyField(Address, related_name='bcc', **KEYFIELD_DEFAULTS)
    reply_to = models.ForeignKey(Address, related_name='reply_to', **KEYFIELD_DEFAULTS)

    def clone(self):
        """Clone and return a Mail

        Use this to send the same MailBody to several sets of recipients.
        """

        newself = super(Mail, self).clone()
        newself.recipients = self.recipients.all()
        newself.ccs = self.ccs.all()
        newself.bccs = self.bccs.all()
        return newself

    @property
    def subject(self):
        return self.content.subject

    @property
    def body(self):
        return self.content.body

    def attach_signature(self, context=None):
        "Attach signature, if any"

        if self.signature:
            return self.signature.attach(context)
        return u''

    def make_content(self, context=None):
        "Generate the content (body + signature) from django templates and context"

        body = _render_from_string(self.content.body, context)
        return body + self.attach_signature()

    def make_subject(self, context=None):
        "Generate the subject from a django template and context"

        return _render_from_string(self.content.subject, context)

    def get_reply_to(self, reply_to=u''):
        "Reply-To may be empty"

        if not reply_to and self.reply_to:
            return unicode(self.reply_to)
        return reply_to

    def get_sender(self, sender=None):
        "Sender may not be empty"

        if not sender:
            if self.sender:
                return unicode(self.sender)
        else:
            return sender
        raise MailrobotNoSenderError("Mail must have a sender")

    def _get_addresses(self, attribute, additional=(), required=False):
        "Merge the addresses of field <attribute> with list in <additional>"

        attribute = getattr(self, attribute)
        addresses = ()
        if attribute:
            addresses = set([unicode(row) for row in attribute.all()])
            addresses = addresses | set(additional)
        if required and not addresses:
            raise MailrobotNoRecipientsError('No recipient addresses!')
        return addresses

    def get_recipients(self, additional=(), required=True):
        """Get recipients for To: and ensures there is at least one.

        Email lacking anything in To: is likely spam."""

        try:
            return self._get_addresses('recipients', additional, required)
        except MailrobotNoRecipientsError as e:
            warnings.warn('Beware: %s An empty "To:" looks spammy' % e.args[0])
            return self._get_addresses('recipients', additional, required=False)

    def get_ccs(self, additional=()):
        """Get recipients for CC:

        May be empty."""

        return self._get_addresses('ccs', additional)

    def get_bccs(self, additional=()):
        """Get recipients for BCC:

        May be empty."""

        return self._get_addresses('bccs', additional)

    def validate_addresses(self, sender=None, recipients=(), ccs=(), bccs=()):
        """Validates that there is one sender and at least one recipient"""
        sender = self.get_sender(sender)
        recipients = self.get_recipients(recipients, required=False)
        ccs = self.get_ccs(ccs)
        bccs = self.get_bccs(bccs)
        if not sender:
            raise MailrobotNoSenderError, "Invalid Email: Lacks sender"
        if not (recipients | ccs | bccs):
            raise MailrobotNoRecipientsError, "Invalid Email: Has no recipients"
        return True

    def make_message(self, sender=None, recipients=(), ccs=(), bccs=(), reply_to=None, headers=None, context=None):
        """Generate a django.core.mail.EmailMessage

        **sender** and **reply_to** may be overridden.
        **recipients**, **ccs** and **bccs** may be supplemented.

        Verfies that there is a sender and at least one recipient.
        """

        if not headers:
            headers = {}
        sender = self.get_sender(sender)
        reply_to = self.get_reply_to(reply_to)
        recipients = self.get_recipients(recipients)
        ccs = self.get_ccs(ccs)
        bccs = self.get_bccs(bccs)

        sendable = self.validate_addresses(sender, recipients, ccs, bccs)

        if reply_to:
            headers['Reply-To'] = reply_to

        subject = self.make_subject(context)
        content = self.make_content(context)
        message = EmailMessage(
            subject=subject,
            body=content,
            from_email=sender,
            to=recipients,
            cc=ccs,
            bcc=bccs,
            headers=headers
        )
        return message

    def send(self, **kwargs):
        "Use django's email backend system to send the Mail"

        message = self.make_message(**kwargs)
        message.send()

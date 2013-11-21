from django.db import models
from django.template import Context, Template
from django.core.mail import EmailMessage
from django.utils.text import slugify

def _render_from_string(templatestring, context=None):
    if context is None:
        context = {}
    template = Template(templatestring)
    return template.render(Context(context))

class NameManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

class AbstractNamedModel(models.Model):
    name = models.SlugField(max_length=40, unique=True)

    objects = NameManager()

    class Meta:
        abstract = True

    def natural_key(self):
        return self.name

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
    sig = models.TextField()

    def __unicode__(self):
        return self.name

class MailBody(AbstractNamedModel):
    subject = models.CharField(max_length=66, unique=True)
    body = models.TextField()

    class Meta:
        verbose_name_plural = 'mailbodies'

    def __unicode__(self):
        return self.subject

class Mail(AbstractNamedModel):
    KEYFIELD_DEFAULTS = {
        'null': True,
        'blank': True,
    }

    content = models.ForeignKey(MailBody, on_delete=models.CASCADE, related_name='mail')
    signature = models.ForeignKey(Signature, null=True, related_name='mail')
    sender = models.ForeignKey(Address, related_name='sender', **KEYFIELD_DEFAULTS)
    recipients = models.ManyToManyField(Address, related_name='recipients', **KEYFIELD_DEFAULTS)
    ccs = models.ManyToManyField(Address, related_name='cc', **KEYFIELD_DEFAULTS)
    bccs = models.ManyToManyField(Address, related_name='bcc', **KEYFIELD_DEFAULTS)
    reply_to = models.ForeignKey(Address, related_name='reply_to', **KEYFIELD_DEFAULTS)

    def __unicode__(self):
        return self.subject

    @property
    def subject(self):
        return self.content.subject

    @property
    def body(self):
        return self.content.body

    def make_content(self, context=None):
        body = _render_from_string(self.content.body, context)
        if self.signature:
            signature = _render_from_string(self.signature.sig, context)
            return "%s\n-- \n%s" % (body, signature)
        return body

    def make_subject(self, context=None):
        return _render_from_string(self.content.subject, context)

    def get_reply_to(self):
        if self.reply_to:
            return self.reply_to.address
        return u''

    def _get_addresses(self, attribute, additional=()):
        attribute = getattr(self, attribute)
        addresses = ()
        if attribute:
            addresses = set([row[0] for row in attribute.values('address')])
            addresses = addresses | set(additional)
        return addresses

    def _get_pp_addresses(self, attribute):
        attribute = getattr(self, attribute)
        if attribute:
            return [unicode(row) for row in attribute.all()]
        return ()

    def get_recipients(self, additional=()):
        return self._get_addresses('recipients', additional)

    def get_ccs(self, additional=()):
        return self._get_addresses('ccs', additional)

    def get_bccs(self, additional=()):
        return self._get_addresses('bccs', additional)

    def make_message(self, sender=None, recipients=(), ccs=(), bccs=(), reply_to=None, context=None):
        if not sender:
            sender = self.sender.address
        if not reply_to:
            reply_to = self.get_reply_to()
        recipients = self.get_recipients(recipients)
        ccs = self.get_ccs(ccs)
        bccs = self.get_bccs(bccs)

        headers = {
            'Reply-To': reply_to,
        }

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
        message = self.make_message(**kwargs)
        message.send()

from __future__ import unicode_literals

from django.test import TestCase

from mailrobot.models import Mail, MailBody, Signature, Address
from mailrobot.models import MailrobotError, MailrobotNoSenderError, MailrobotNoRecipientsError


HELLO_WORLD_BODY_TEMPLATE = """Hello, {{ world|default:"World" }}!

This is a test of mail robot."""

HELLO_WORLD_SUBJECT_TEMPLATE = 'Hello, {{ world|default:"World" }}!'

class CloneTest(TestCase):

    def setUp(self):
        self.mailbody = MailBody(subject='test', body='test', name='test')
        self.mailbody.save()
        self.mail = Mail(content=self.mailbody, name='test')
        self.mail.save()
        self.address = Address(address='postmaster@example.com')
        self.address.save()
        self.name_max_length = MailBody.NAME_MAX_LENGTH

    def test_default_clone(self):
        model = self.mailbody
        clone = model.clone()
        self.assertNotEqual(model, clone)

    def test_cloned_long_name(self):
        longname = 'x' * MailBody.NAME_MAX_LENGTH
        model = self.mailbody
        model.name = longname
        clone = model.clone()
        self.assertNotEqual(model, clone)
        self.assertLessEqual(len(clone.name), MailBody.NAME_MAX_LENGTH)

    def test_mail_clone(self):
        model = self.mail
        model.sender = self.address
        model.recipients.set([self.address])
        model.save()
        clone = model.clone()
        self.assertNotEqual(model, clone)
        self.assertEqual(set(clone.recipients.all()), set(model.recipients.all()))

class MailTest(TestCase):

    def setUp(self):
        self.mailbody = MailBody(
            subject=HELLO_WORLD_SUBJECT_TEMPLATE,
            body=HELLO_WORLD_BODY_TEMPLATE,
            name='hello-world',
        )
        self.mailbody.save()

        self.empty_sig = Signature(name='empty', sig='').save()
        self.simple_sig = Signature(name='simple', sig='simple').save()
        self.complex_sig = Signature(name='complex', sig='{{ complex }}').save()

        self.mail = Mail(
            content=self.mailbody,
            name='hello-world',
        )
        self.mail.save()

        self.simple_address = Address(
            address='postmaster@example.com'
        )
        self.simple_address.save()

        self.complex_address = Address(
            address='abuse@example.com',
            comment='CERT'
        )
        self.complex_address.save()

    def test_no_signature(self):
        expected_result = ''
        self.assertEqual('', self.mail.attach_signature())

    def test_no_sender_no_recipients(self):
        with self.assertRaises(MailrobotError):
            self.mail.make_message()

    def test_has_sender_lacks_recipients(self):
        with self.assertRaises(MailrobotNoRecipientsError):
            self.mail.make_message(sender=self.simple_address)

    def test_no_sender_one_recipient(self):
        with self.assertRaises(MailrobotNoSenderError):
            self.mail.make_message(recipients=[self.simple_address])

    def test_validate_one_simple_recipient(self):
        self.mail.sender = self.simple_address
        self.mail.save()
        recipients = (self.simple_address,)
        result = self.mail.validate_addresses(recipients=recipients)
        self.assertTrue(result)

    def test_validate_one_complex_recipient(self):
        self.mail.sender = self.simple_address
        self.mail.save()
        recipients = (self.complex_address,)
        result = self.mail.validate_addresses(recipients=recipients)
        self.assertTrue(result)

    def test_validate_two_recipients(self):
        self.mail.sender = self.simple_address
        self.mail.save()
        recipients = (self.simple_address, self.complex_address)
        result = self.mail.validate_addresses(recipients=recipients)
        self.assertTrue(result)

class SignatureTest(TestCase):

    SIG_TEMPLATE = '\r\n\r\n\r\n-- \r\n%s'

    def test_empty_signature(self):
        sig = Signature(name='test1', sig='')
        sig.save()
        expected_result = ''
        self.assertEqual(expected_result, sig.attach())

    def test_simple_signature(self):
        content = 'foo'
        sig = Signature(name='test1', sig=content)
        expected_result = self.SIG_TEMPLATE % content
        self.assertEqual(expected_result, sig.attach())

    def test_complex_signature(self):
        content = 'foo{{ word }}foo'
        context = {'word': 'foo'}
        sig = Signature(name='test1', sig=content)
        expected_result = self.SIG_TEMPLATE % 'foofoofoo'
        self.assertEqual(expected_result, sig.attach(context))

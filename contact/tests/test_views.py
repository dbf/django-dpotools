from unittest import mock
from io import StringIO

from django.test import TestCase
from django.test import Client
from django.test import RequestFactory
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import InMemoryUploadedFile

from contact.views import ContactView


class ContactViewsTest(TestCase):
    fixtures = ["kuno.json"]
    subjstr = "x" * 30
    msgstr = "x" * 200
    basic_form_data = {
        "name": "",
        "email": "",
        "subject": subjstr,
        "message": msgstr,
    }
    text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit,
           sed do eiusmod tempor incididunt ut labore et dolore magna
           aliqua.
           """

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_contact_template(self):
        response = self.client.get(reverse("contact:contact"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contact/contact.html")
        self.assertIs(response.resolver_match.func.view_class, ContactView)

    def test_contact_success_template(self):
        response = self.client.get(reverse("contact:contact_success"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contact/contact_success.html")

    def test_contact_error_template(self):
        response = self.client.get(reverse("contact:contact_error"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contact/contact_error.html")

    def test_get_user_data_for_logged_in_users(self):
        self.client.login(username="kuno", password="kuno")
        response = self.client.get("/contact/")
        self.assertContains(
            response, "form", count=None, status_code=200, msg_prefix="", html=False
        )
        self.assertEqual(response.context["form"].initial["name"], "Dr. Klöbner")
        self.assertEqual(
            response.context["form"].initial["email"], "kuno@some-entity.org"
        )

    def test_contact_send_email_without_attachment(self):
        request = self.factory.post("/contact/", data=self.basic_form_data)
        request.user = AnonymousUser()
        response = ContactView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/contact/success/")
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.subjstr, mail.outbox[0].subject)
        self.assertIn(self.msgstr, mail.outbox[0].body)

    def test_contact_send_email_with_attachment(self):
        file = StringIO()
        file.write(self.text)
        file.seek(0)
        attachment_form_data = {
            "name": "",
            "email": "",
            "subject": self.subjstr,
            "message": self.msgstr,
            "attachment": InMemoryUploadedFile(
                file, None, "example.txt", "text/plain", len(file.getvalue()), None
            ),
        }
        request = self.factory.post("/contact/", data=attachment_form_data)
        request.user = AnonymousUser()
        response = ContactView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Lorem ipsum", mail.outbox[0].attachments[0][1])

    @mock.patch("contact.views.EmailMessage.send")
    def test_contact_send_email_fails_with_exception(self, send_mock):
        send_mock.side_effect = Exception()
        request = self.factory.post("/contact/", data=self.basic_form_data)
        request.user = AnonymousUser()
        response = ContactView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/contact/error/")

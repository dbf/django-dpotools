from io import BytesIO, StringIO

from PIL import Image

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from django.conf import settings
from contact.forms import ContactForm


class ContactFormTest(TestCase):
    name = "Dr. Klöbner"
    name_empty = ""
    email = "kloebner@some-entity.org"
    email_empty = ""
    subject = "x" * 30
    message = "x" * 200

    def test_contactform_with_sender_data(self):
        form_data = {
            "name": self.name,
            "email": self.email,
            "subject": self.subject,
            "message": self.message,
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_contactform_without_sender_data(self):
        form_data = {
            "name": self.name_empty,
            "email": self.email_empty,
            "subject": self.subject,
            "message": self.message,
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_contactform_with_missing_subject_or_message(self):
        form_data = {
            "name": self.name_empty,
            "email": self.email_empty,
            "subject": self.subject,
            "message": self.message,
        }
        form_data["subject"] = ""
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        form_data["subject"] = self.subject
        form_data["message"] = ""
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_contactform_with_text_attachment(self):
        form_data = {
            "name": self.name_empty,
            "email": self.email_empty,
            "subject": self.subject,
            "message": self.message,
        }
        text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit,
               sed do eiusmod tempor incididunt ut labore et dolore magna
               aliqua.
               """
        file = StringIO()
        file.write(text)
        file.seek(0)
        text_data = {
            "attachment": InMemoryUploadedFile(
                file, None, "example.txt", "text/plain", len(file.getvalue()), None
            )
        }
        form = ContactForm(data=form_data, files=text_data)
        self.assertTrue(form.is_valid())

    def test_contactform_with_pdf_attachment(self):
        form_data = {
            "name": self.name_empty,
            "email": self.email_empty,
            "subject": self.subject,
            "message": self.message,
        }
        pdf = """%PDF-1.0
              1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
              2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
              3 0 obj<</Type/Page/MediaBox[0 0 3 3]>>endobj
              xref
              0 4
              0000000000 65535 f
              0000000010 00000 n
              0000000053 00000 n
              0000000102 00000 n
              trailer<</Size 4/Root 1 0 R>>
              startxref
              149
              %EOF
              """
        file = StringIO()
        file.write(pdf)
        file.seek(0)
        pdf_data = {
            "attachment": InMemoryUploadedFile(
                file, None, "example.pdf", "application/pdf", len(file.getvalue()), None
            )
        }
        form = ContactForm(data=form_data, files=pdf_data)
        self.assertTrue(form.is_valid())

    def test_contactform_with_correct_imgfmt_attachment(self):
        form_data = {
            "name": self.name,
            "email": self.email,
            "subject": self.subject,
            "message": self.message,
        }
        img = Image.new(mode="RGB", size=(10, 10))
        file = BytesIO()
        img.save(file, "JPEG")
        file.seek(0)
        image_data = {
            "attachment": InMemoryUploadedFile(
                file, None, "black.jpg", "image/jpeg", len(file.getvalue()), None
            )
        }
        form = ContactForm(data=form_data, files=image_data)
        self.assertTrue(form.is_valid())

    def test_contactform_with_wrong_imgfmt_attachment(self):
        form_data = {
            "name": self.name,
            "email": self.email,
            "subject": self.subject,
            "message": self.message,
        }
        img = Image.new(mode="RGB", size=(10, 10))
        file = BytesIO()
        img.save(file, "GIF")
        file.seek(0)
        # libmagic should not struggle over this, it's a GIF anyway
        image_data = {
            "attachment": InMemoryUploadedFile(
                file, None, "black.jpg", "image/jpeg", len(file.getvalue()), None
            )
        }
        form = ContactForm(data=form_data, files=image_data)
        self.assertFalse(form.is_valid())

    def test_contactform_with_attachment(self):
        form_data = {
            "name": self.name,
            "email": self.email,
            "subject": self.subject,
            "message": self.message,
        }
        img = Image.new(mode="RGB", size=(10, 10))
        file = BytesIO()
        img.save(file, "PNG")
        file.seek(0)
        image_data = {
            "attachment": InMemoryUploadedFile(
                file,
                None,
                "black.png",
                "image/png",
                int(settings.CONTACT_MAX_FILESIZE + 1),
                None,
            )
        }
        form = ContactForm(data=form_data, files=image_data)
        self.assertFalse(form.is_valid())
        image_data = {
            "attachment": InMemoryUploadedFile(
                file,
                None,
                "black.png",
                "image/png",
                int(settings.CONTACT_MAX_FILESIZE - 1),
                None,
            )
        }
        form = ContactForm(data=form_data, files=image_data)
        self.assertTrue(form.is_valid())

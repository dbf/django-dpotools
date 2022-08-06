import magic
from django import forms
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit


class ContactForm(forms.Form):
    """DPO contact form with crispy FormHelper and custom cleaning"""

    email_regex = r"^[\w\.\-\+]+\@[\w\.\-]+\.[a-z]{2,6}$"

    name = forms.CharField(label=_("Sender"), max_length=60, required=False)
    email = forms.CharField(
        label=_("Email"),
        max_length=100,
        required=False,
        validators=[
            RegexValidator(
                regex=email_regex,
                message=_(
                    "If you decide to state your Email address, please make sure it is valid."
                ),
            )
        ],
    )
    subject = forms.CharField(
        label=_("Subject"), min_length=30, max_length=70, required=True
    )
    message = forms.CharField(
        widget=forms.Textarea,
        label=_("Message"),
        min_length=200,
        max_length=8192,
        required=True,
    )
    attachment = forms.FileField(
        label=_("File attachment"),
        required=False,
        widget=forms.FileInput(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    "name",
                    "email",
                    "subject",
                    "message",
                    "attachment",
                    css_class="form-group col-md-8 mb-0",
                ),
            ),
            Row(
                Submit("submit", _("Send"), css_class="btn btn-primary"),
            ),
        )

    def clean(self):
        err_0 = _("File upload is restricted to MIME types ") + ", ".join(
            str(mt) for mt in settings.CONTACT_ALLOWED_MIMETYPES
        )
        err_1 = (
            _("File upload is restricted to a file size of ")
            + str(int(settings.CONTACT_MAX_FILESIZE / 1048576) - 1)
            + " Megabytes."
        )
        attachment = self.cleaned_data.get("attachment")
        if attachment is not None:
            is_allowed = 0
            mimetype = magic.from_buffer(attachment.read(2048), mime=True)
            attachment.seek(0)
            for allowedmt in settings.CONTACT_ALLOWED_MIMETYPES:
                if allowedmt in mimetype:
                    is_allowed = 1
            if is_allowed != 1:
                raise forms.ValidationError(err_0)
        if attachment is not None:
            if attachment.size > settings.CONTACT_MAX_FILESIZE:
                raise forms.ValidationError(err_1)

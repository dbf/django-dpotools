import logging
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import ContactForm

logger = logging.getLogger(__name__)


class ContactView(FormView):
    """DPO contact form view incl. forwarding form data as email"""

    form_class = ContactForm
    template_name = "contact/contact.html"
    success_url = reverse_lazy("contact:contact_success")

    def get_initial(self):
        """Get user name and email, in case form is used by
        authenticated user
        """
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial.update({"name": self.request.user.get_full_name()})
            initial.update({"email": self.request.user.email})
        return initial

    def form_valid(self, form):
        """Process valid form's contents, construct EmailMessage()
        object and finally try to send it to the DPO
        """
        name = form.cleaned_data["name"]
        if not name:
            name = settings.CONTACT_EMPTY_SENDER_NAME
        email = form.cleaned_data["email"]
        if not email:
            email = settings.CONTACT_EMPTY_SENDER_EMAIL
        subject = form.cleaned_data["subject"]
        message = form.cleaned_data["message"]
        attachment = None
        if "attachment" in self.request.FILES:
            attachment = self.request.FILES["attachment"]
        mailobj = EmailMessage(
            settings.CONTACT_SUBJ_PREFIX + subject,
            settings.CONTACT_WARNING + "\n\n" + message,
            name + " " + "<" + email + ">",
            [settings.CONTACT_RECIPIENT],
        )
        if attachment is not None:
            mailobj.attach(attachment.name, attachment.read(), attachment.content_type)
        try:
            mailobj.send(fail_silently=False)
        # except BadHeaderError:
        #    pass
        except Exception as err:
            # TBD: mail admin
            logger.error(
                "EXCEPTION caught at ContactView form_valid() while sending mail"
            )
            logger.error(err)
            return redirect("contact:contact_error")
        finally:
            # the logger.warning line below will log a message to the
            # webserver's error log (at least when using Apache/WSGI)
            # that can be used to create a fail2ban jail
            # otherwise (the default) just "let it pass"
            pass
            # logger.warning("f2b-ban-KWVnPr3j")
        return super().form_valid(form)


class ContactSuccessView(TemplateView):
    template_name = "contact/contact_success.html"


class ContactErrorView(TemplateView):
    template_name = "contact/contact_error.html"

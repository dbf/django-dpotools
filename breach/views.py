from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.views.generic import DetailView
from django.views.generic.edit import DeleteView, CreateView
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404

from django_weasyprint import WeasyTemplateResponseMixin

from .models import (
    Breach,
    BreachDataController,
    BreachTimeLine,
    BreachDescription,
    BreachAffectedData,
    BreachAffectedSubjects,
    BreachConsequences,
    BreachMeasures,
    BreachCommunication,
)

from .forms import (
    BreachForm,
    BreachDataControllerForm,
    BreachTimeLineForm,
    BreachDescriptionForm,
    BreachAffectedDataForm,
    BreachAffectedSubjectsForm,
    BreachConsequencesForm,
    BreachMeasuresForm,
    BreachCommunicationForm,
)


class BreachUserPassesMixin(UserPassesTestMixin):
    def test_func(self):
        is_allowed = False
        breachslug = self.kwargs.get("slug")
        breach = get_object_or_404(Breach, slug=breachslug)
        current_user = breach.user or None
        if self.request.user.groups.filter(name="dpo").exists():
            is_allowed = True
        if self.request.user.is_superuser:
            is_allowed = True
        if self.request.user and self.request.user == current_user:
            is_allowed = True
        return is_allowed


class BreachHintsView(LoginRequiredMixin, TemplateView):
    template_name = "breach/breach_hints.html"


class MyBreachesView(LoginRequiredMixin, ListView):
    model = Breach
    template_name = "breach/breach_view.html"
    context_object_name = "breach"
    paginate_by = 12

    def get_queryset(self):
        return Breach.objects.filter(user=self.request.user).order_by("slug")


class AllBreachesView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """staff user must be logged in and member of group "dpo" to view
    all breaches
    """

    model = Breach
    template_name = "breach/breach_view_all.html"
    context_object_name = "breach"
    # paginate_by = 12

    def test_func(self):
        is_allowed = False
        if self.request.user.groups.filter(name="dpo").exists():
            is_allowed = True
        if self.request.user.is_superuser:
            is_allowed = True
        return is_allowed

    def get_queryset(self):
        return Breach.objects.all


class BreachDetailView(LoginRequiredMixin, BreachUserPassesMixin, DetailView):
    model = Breach
    template_name = "breach/breach_htmltemplate.html"
    context_object_name = "breach"


class BreachDetailPDFView(WeasyTemplateResponseMixin, BreachDetailView):
    template_name = "breach/breach_pdftemplate.html"
    pdf_stylesheets = [
        settings.BASE_DIR / "breach/static/breach/breach_pdftemplate.css",
    ]
    pdf_attachment = False

    def get_pdf_filename(self):
        if self.object:
            breachname = _("breach") + "-" + str(self.object)
        else:
            breachname = _("breach")
        return "{breachname}-{at}.pdf".format(
            at=timezone.now().strftime("%Y%m%d"), breachname=breachname
        )


class BreachDeleteView(LoginRequiredMixin, BreachUserPassesMixin, DeleteView):
    model = Breach
    template_name = "breach/breach_delete_confirmation.html"
    success_url = reverse_lazy("breach:my_breaches")

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return redirect("breach:my_breaches")
        return super().post(request, *args, **kwargs)


class AllBreachDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Breach
    template_name = "breach/breach_delete_confirmation.html"
    success_url = reverse_lazy("breach:all_breaches")

    def test_func(self):
        is_allowed = False
        if self.request.user.groups.filter(name="dpo").exists():
            is_allowed = True
        if self.request.user.is_superuser:
            is_allowed = True
        return is_allowed

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return redirect("breach:all_breaches")
        return super().post(request, *args, **kwargs)


class BreachEditView(LoginRequiredMixin, BreachUserPassesMixin, DetailView):
    model = Breach
    template_name = "breach/breach_edit.html"
    context_object_name = "breach"


class BreachCreateSimpleFormView(CreateView):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        breachslug = self.kwargs.get("slug")
        breach = get_object_or_404(Breach, slug=breachslug)
        try:
            existing_instance = self.model.objects.get(breach=breach)
        except self.model.DoesNotExist:
            existing_instance = None
        if existing_instance:
            kwargs["instance"] = existing_instance
        return kwargs

    def form_valid(self, form):
        breachslug = self.kwargs.get("slug")
        breach = get_object_or_404(Breach, slug=breachslug)
        form.instance.breach = breach
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breachslug = self.kwargs.get("slug")
        context["breach"] = get_object_or_404(Breach, slug=breachslug)
        return context

    def get_success_url(self):
        return reverse("breach:breach_detail_edit", args=[self.kwargs["slug"]])


class BreachCreateView(LoginRequiredMixin, CreateView):
    form_class = BreachForm
    template_name = "breach/breach_create_slug.html"
    model = Breach

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("breach:my_breaches")


class BreachCreateDconView(
    LoginRequiredMixin, BreachUserPassesMixin, BreachCreateSimpleFormView
):
    form_class = BreachDataControllerForm
    model = BreachDataController
    template_name = "breach/breach_create_dcon.html"


class BreachCreateBtlView(
    LoginRequiredMixin, BreachUserPassesMixin, BreachCreateSimpleFormView
):
    form_class = BreachTimeLineForm
    model = BreachTimeLine
    template_name = "breach/breach_create_btl.html"


class BreachCreateBdescView(
    LoginRequiredMixin, BreachUserPassesMixin, BreachCreateSimpleFormView
):
    form_class = BreachDescriptionForm
    model = BreachDescription
    template_name = "breach/breach_create_bdesc.html"


class BreachCreateBaffdView(
    LoginRequiredMixin, BreachUserPassesMixin, BreachCreateSimpleFormView
):
    form_class = BreachAffectedDataForm
    model = BreachAffectedData
    template_name = "breach/breach_create_baffd.html"


class BreachCreateBaffsView(
    LoginRequiredMixin, BreachUserPassesMixin, BreachCreateSimpleFormView
):
    form_class = BreachAffectedSubjectsForm
    model = BreachAffectedSubjects
    template_name = "breach/breach_create_baffs.html"


class BreachCreateBconsView(
    LoginRequiredMixin, BreachUserPassesMixin, BreachCreateSimpleFormView
):
    form_class = BreachConsequencesForm
    model = BreachConsequences
    template_name = "breach/breach_create_bcons.html"


class BreachCreateBmeasuresView(
    LoginRequiredMixin, BreachUserPassesMixin, BreachCreateSimpleFormView
):
    form_class = BreachMeasuresForm
    model = BreachMeasures
    template_name = "breach/breach_create_bmeasures.html"


class BreachCreateBcommView(
    LoginRequiredMixin, BreachUserPassesMixin, BreachCreateSimpleFormView
):
    form_class = BreachCommunicationForm
    model = BreachCommunication
    template_name = "breach/breach_create_bcomm.html"

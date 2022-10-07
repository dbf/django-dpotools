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

from extra_views import ModelFormSetView

from .models import (
    Rpa,
    ProcessingActivityName,
    DataController,
    JointController,
    DataProtectionOfficer,
    InternallyResponsibleDept,
    CategoryOfPersonalData,
    CategoriesOfPersonalDataOrigin,
    PurposeAndLegalBasis,
    DataSubject,
    TimeLimitForErasure,
    CategoryOfRecipients,
    TransferToThirdCountry,
    AccessGroup,
    Transparency,
    DataProcessor,
    PrivacyImpactAssessment,
    TOM,
    RPAAnnex,
)

from .forms import (
    RpaForm,
    ProcessingActivityNameForm,
    DataControllerForm,
    JointControllerForm,
    DataProtectionOfficerForm,
    InternallyResponsibleDeptForm,
    CategoryOfPersonalDataForm,
    CategoryOfPersonalDataFormSet,
    CategoriesOfPersonalDataOriginForm,
    PurposeAndLegalBasisForm,
    DataSubjectForm,
    TimeLimitForErasureForm,
    CategoryOfRecipientsForm,
    TransferToThirdCountryForm,
    AccessGroupForm,
    TransparencyForm,
    DataProcessorForm,
    PrivacyImpactAssessmentForm,
    TOMForm,
    RPAAnnexForm,
    RPAAnnexFormSet,
)

from .forms import (
    CpdModelMultipleChoiceField,
    CPD_CHOICES,
)


class RPAGenUserPassesMixin(UserPassesTestMixin):
    def test_func(self):
        is_allowed = False
        rpaslug = self.kwargs.get("slug")
        rpa = get_object_or_404(Rpa, slug=rpaslug)
        current_user = rpa.user or None
        if self.request.user.groups.filter(name="dpo").exists():
            is_allowed = True
        if self.request.user.is_superuser:
            is_allowed = True
        if self.request.user and self.request.user == current_user:
            is_allowed = True
        return is_allowed


class RPAHomeView(LoginRequiredMixin, TemplateView):
    template_name = "rpa/rpa_home.html"


class RPAHintsView(LoginRequiredMixin, TemplateView):
    template_name = "rpa/rpa_hints.html"


class MyRPAsView(LoginRequiredMixin, ListView):
    model = Rpa
    template_name = "rpa/rpa_view.html"
    context_object_name = "rpa"
    paginate_by = 12

    def get_queryset(self):
        return Rpa.objects.filter(user=self.request.user).order_by("slug")


class AllRPAsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """staff user must be logged in and member of group "dpo" to view all RPAs"""

    model = Rpa
    template_name = "rpa/rpa_view_all.html"
    context_object_name = "rpa"
    # paginate_by = 12

    def test_func(self):
        is_allowed = False
        if self.request.user.groups.filter(name="dpo").exists():
            is_allowed = True
        if self.request.user.is_superuser:
            is_allowed = True
        return is_allowed

    def get_queryset(self):
        return Rpa.objects.all


class RPADetailView(LoginRequiredMixin, RPAGenUserPassesMixin, DetailView):
    model = Rpa
    template_name = "rpa/rpa_htmltemplate.html"
    context_object_name = "rpa"


class RPADetailPDFView(WeasyTemplateResponseMixin, RPADetailView):
    template_name = "rpa/rpa_pdftemplate.html"
    pdf_stylesheets = [
        settings.BASE_DIR / "rpa/static/rpa/rpa_pdftemplate.css",
    ]
    pdf_attachment = False

    def get_pdf_filename(self):
        if self.object:
            rpaname = _("rpa") + "-" + str(self.object)
        else:
            rpaname = _("rpa")
        return "{rpaname}-{at}.pdf".format(
            at=timezone.now().strftime("%Y%m%d"), rpaname=rpaname
        )


class RPADeleteView(LoginRequiredMixin, RPAGenUserPassesMixin, DeleteView):
    model = Rpa
    template_name = "rpa/rpa_delete_confirmation.html"
    success_url = reverse_lazy("rpa:my_rpas")

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return redirect("rpa:my_rpas")
        return super().post(request, *args, **kwargs)


class AllRPADeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Rpa
    template_name = "rpa/rpa_delete_confirmation.html"
    success_url = reverse_lazy("rpa:all_rpas")

    def test_func(self):
        is_allowed = False
        if self.request.user.groups.filter(name="dpo").exists():
            is_allowed = True
        if self.request.user.is_superuser:
            is_allowed = True
        return is_allowed

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return redirect("rpa:all_rpas")
        return super().post(request, *args, **kwargs)


class RPAEditView(LoginRequiredMixin, RPAGenUserPassesMixin, DetailView):
    model = Rpa
    template_name = "rpa/rpa_edit.html"
    context_object_name = "rpa"


class RPACreateSimpleFormView(CreateView):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        rpaslug = self.kwargs.get("slug")
        rpa = get_object_or_404(Rpa, slug=rpaslug)
        try:
            existing_instance = self.model.objects.get(rpa=rpa)
        except self.model.DoesNotExist:
            existing_instance = None
        if existing_instance:
            kwargs["instance"] = existing_instance
        return kwargs

    def form_valid(self, form):
        rpaslug = self.kwargs.get("slug")
        rpa = get_object_or_404(Rpa, slug=rpaslug)
        form.instance.rpa = rpa
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rpaslug = self.kwargs.get("slug")
        context["rpa"] = get_object_or_404(Rpa, slug=rpaslug)
        return context

    def get_success_url(self):
        return reverse("rpa:rpa_detail_edit", args=[self.kwargs["slug"]])


class RPACreateSimpleFormsetView(ModelFormSetView):
    def get_queryset(self):
        rpaslug = self.kwargs.get("slug")
        rpa = get_object_or_404(Rpa, slug=rpaslug)
        return super().get_queryset().filter(rpa=rpa)

    def formset_valid(self, formset):
        rpaslug = self.kwargs.get("slug")
        rpa = get_object_or_404(Rpa, slug=rpaslug)
        for form in formset:
            form.instance.rpa = rpa
        return super().formset_valid(formset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rpaslug = self.kwargs.get("slug")
        context["rpa"] = get_object_or_404(Rpa, slug=rpaslug)
        return context

    def get_success_url(self):
        return reverse("rpa:rpa_detail_edit", args=[self.kwargs["slug"]])


class RPACreateChoiceFormsetView(ModelFormSetView):
    def construct_formset(self):
        formset = super().construct_formset()
        rpaslug = self.kwargs.get("slug")
        rpa = get_object_or_404(Rpa, slug=rpaslug)
        choice_field = self.kwargs.get("choice_field", None)
        for form in formset:
            form.fields[choice_field] = CpdModelMultipleChoiceField(
                queryset=CategoryOfPersonalData.objects.filter(rpa=rpa),
                widget=forms.CheckboxSelectMultiple,
                label=CPD_CHOICES,
                required=False,
            )
            if form.instance.id:
                previously_selected = []
                for i in form.instance.cpd.all():
                    previously_selected.append(i.pk)
                form.initial[choice_field] = previously_selected
        return formset

    def get_queryset(self):
        rpaslug = self.kwargs.get("slug")
        rpa = get_object_or_404(Rpa, slug=rpaslug)
        return super().get_queryset().filter(rpa=rpa)

    def formset_valid(self, formset):
        rpaslug = self.kwargs.get("slug")
        rpa = get_object_or_404(Rpa, slug=rpaslug)
        for form in formset:
            form.instance.rpa = rpa
        return super().formset_valid(formset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rpaslug = self.kwargs.get("slug")
        rpa = get_object_or_404(Rpa, slug=rpaslug)
        cpd = CategoryOfPersonalData.objects.filter(rpa=rpa)
        context["rpa"] = rpa
        context["cpd"] = cpd
        return context

    def get_success_url(self):
        return reverse("rpa:rpa_detail_edit", args=[self.kwargs["slug"]])


class RPACreateView(LoginRequiredMixin, CreateView):
    form_class = RpaForm
    template_name = "rpa/rpa_create_slug.html"
    model = Rpa

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("rpa:my_rpas")


class RPACreateRpanmView(
    LoginRequiredMixin, RPAGenUserPassesMixin, RPACreateSimpleFormView
):
    form_class = ProcessingActivityNameForm
    model = ProcessingActivityName
    template_name = "rpa/rpa_create_name.html"


class RPACreateDconView(
    LoginRequiredMixin, RPAGenUserPassesMixin, RPACreateSimpleFormView
):
    form_class = DataControllerForm
    model = DataController
    template_name = "rpa/rpa_create_dcon.html"


class RPACreateJconView(
    LoginRequiredMixin, RPAGenUserPassesMixin, RPACreateSimpleFormView
):
    form_class = JointControllerForm
    model = JointController
    template_name = "rpa/rpa_create_jcon.html"


class RPACreateDpoView(
    LoginRequiredMixin, RPAGenUserPassesMixin, RPACreateSimpleFormView
):
    form_class = DataProtectionOfficerForm
    model = DataProtectionOfficer
    template_name = "rpa/rpa_create_dpo.html"


class RPACreateIrdView(
    LoginRequiredMixin, RPAGenUserPassesMixin, RPACreateSimpleFormView
):
    form_class = InternallyResponsibleDeptForm
    model = InternallyResponsibleDept
    template_name = "rpa/rpa_create_ird.html"


class RPACreateCpdView(
    LoginRequiredMixin, RPAGenUserPassesMixin, RPACreateSimpleFormsetView
):
    model = CategoryOfPersonalData
    form_class = CategoryOfPersonalDataForm
    formset_class = CategoryOfPersonalDataFormSet
    factory_kwargs = {
        "min_num": 1,
        "max_num": 9,
        "extra": 8,
        "can_order": False,
        "can_delete": True,
    }
    template_name = "rpa/rpa_create_cpd.html"


class RPACreateCpdoView(
    LoginRequiredMixin, RPAGenUserPassesMixin, RPACreateSimpleFormView
):
    form_class = CategoriesOfPersonalDataOriginForm
    model = CategoriesOfPersonalDataOrigin
    template_name = "rpa/rpa_create_cpdo.html"


class RPACreatePlbView(
    LoginRequiredMixin, RPAGenUserPassesMixin, RPACreateSimpleFormView
):
    form_class = PurposeAndLegalBasisForm
    model = PurposeAndLegalBasis
    template_name = "rpa/rpa_create_plb.html"


class RPACreateDSubView(
    LoginRequiredMixin, RPAGenUserPassesMixin, RPACreateChoiceFormsetView
):
    model = DataSubject
    form_class = DataSubjectForm
    factory_kwargs = {
        "min_num": 1,
        "max_num": 9,
        "extra": 8,
        "can_order": False,
        "can_delete": True,
    }
    template_name = "rpa/rpa_create_dsub.html"


class RPACreateTleView(
    LoginRequiredMixin, RPAGenUserPassesMixin, RPACreateChoiceFormsetView
):
    model = TimeLimitForErasure
    form_class = TimeLimitForErasureForm
    factory_kwargs = {
        "min_num": 1,
        "max_num": 5,
        "extra": 4,
        "can_order": False,
        "can_delete": True,
    }
    template_name = "rpa/rpa_create_tle.html"


class RPACreateCrecView(
    LoginRequiredMixin, RPAGenUserPassesMixin, RPACreateChoiceFormsetView
):
    model = CategoryOfRecipients
    form_class = CategoryOfRecipientsForm
    factory_kwargs = {
        "min_num": 1,
        "max_num": 5,
        "extra": 4,
        "can_order": False,
        "can_delete": True,
    }
    template_name = "rpa/rpa_create_crec.html"

    def get_initial(self):
        initial = [
            {"crec_exists": None},
        ]
        return initial


class RPACreateTtcView(
    LoginRequiredMixin, RPAGenUserPassesMixin, RPACreateSimpleFormView
):
    form_class = TransferToThirdCountryForm
    model = TransferToThirdCountry
    template_name = "rpa/rpa_create_ttc.html"


class RPACreateAgrpView(
    LoginRequiredMixin, RPAGenUserPassesMixin, RPACreateChoiceFormsetView
):
    model = AccessGroup
    form_class = AccessGroupForm
    factory_kwargs = {
        "min_num": 1,
        "max_num": 9,
        "extra": 8,
        "can_order": False,
        "can_delete": True,
    }
    template_name = "rpa/rpa_create_agrp.html"


class RPACreateTranView(
    LoginRequiredMixin, RPAGenUserPassesMixin, RPACreateSimpleFormView
):
    form_class = TransparencyForm
    model = Transparency
    template_name = "rpa/rpa_create_tran.html"


class RPACreateDproView(
    LoginRequiredMixin, RPAGenUserPassesMixin, RPACreateSimpleFormView
):
    form_class = DataProcessorForm
    model = DataProcessor
    template_name = "rpa/rpa_create_dpro.html"


class RPACreatePiaView(
    LoginRequiredMixin, RPAGenUserPassesMixin, RPACreateSimpleFormView
):
    form_class = PrivacyImpactAssessmentForm
    model = PrivacyImpactAssessment
    template_name = "rpa/rpa_create_pia.html"


class RPACreateTomView(
    LoginRequiredMixin, RPAGenUserPassesMixin, RPACreateSimpleFormView
):
    form_class = TOMForm
    model = TOM
    template_name = "rpa/rpa_create_tom.html"


class RPACreateAnnexView(
    LoginRequiredMixin, RPAGenUserPassesMixin, RPACreateSimpleFormsetView
):
    model = RPAAnnex
    form_class = RPAAnnexForm
    formset_class = RPAAnnexFormSet
    factory_kwargs = {
        "min_num": 0,
        "max_num": 9,
        "extra": 9,
        "can_order": False,
        "can_delete": True,
    }
    template_name = "rpa/rpa_create_annex.html"

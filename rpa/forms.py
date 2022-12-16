from django import forms
from django.forms import ModelForm, BaseModelFormSet
from django.forms.widgets import NumberInput, Textarea, Select
from django.core.validators import RegexValidator
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from crispy_forms.bootstrap import TabHolder, Tab

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


CPD_CHOICES = _("Categories of personal data choices")


class RpaForm(ModelForm):
    lowercase_only_regex = r"^[a-z0-9\_\-]+$"
    slug = forms.SlugField(
        min_length=8,
        max_length=20,
        label=_('Short name ("slug") for your processing activity:'),
        validators=[
            RegexValidator(
                regex=lowercase_only_regex,
                message=_(
                    "Please use lowercase letters, numbers, hyphens and underscores only."
                ),
            )
        ],
    )
    rpa_bumper = forms.BooleanField(
        required=True,
        initial=False,
        label=_(
            "I am aware of my duty of care to check all information given for correctness and completeness."
        ),
    )

    class Meta:
        HELP_TEXT_CHOICES = (
            (
                "show",
                _("folded out (shown)"),
            ),
            (
                "hide",
                _("folded in (not shown)"),
            ),
        )
        model = Rpa
        fields = ["slug", "rpa_bumper", "helptext_display_default"]
        labels = {
            "helptext_display_default": _("Boxes with help texts shall by default be"),
        }
        widgets = {
            "helptext_display_default": Select(choices=HELP_TEXT_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("slug", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("rpa_bumper", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column(
                    "helptext_display_default", css_class="form-group col-md-6 mb-0"
                ),
                css_class="form-row",
            ),
            Row(
                Submit("submit", _("Submit"), css_class="btn btn-primary"),
            ),
        )


class ProcessingActivityNameForm(ModelForm):
    class Meta:
        model = ProcessingActivityName
        fields = [
            "name",
            "is_new",
            "date_intro",
            "has_changed",
            "date_changed",
            "former_name",
        ]
        labels = {
            "name": _("Processing activity name:"),
            "is_new": _("Is this a new processing activity?"),
            "date_intro": _("Processing activity date of introduction:"),
            "has_changed": _("Is this a changed processing activity?"),
            "date_changed": _("Processing activity date of change:"),
            "former_name": _("Processing activity former name (if changed):"),
        }
        help_texts = {
            "name": _(
                "A descriptive name for your processing activity (including your department name)."
            ),
        }
        widgets = {
            "date_intro": NumberInput(attrs={"type": "date"}),
            "date_changed": NumberInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    "name",
                    TabHolder(
                        Tab(_("New activity"), "is_new", "date_intro"),
                        Tab(
                            _("Changed activity"),
                            "has_changed",
                            "date_changed",
                            "former_name",
                        ),
                    ),
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Submit("submit", _("Submit"), css_class="btn btn-primary"),
            ),
        )

    def clean(self):
        err_0 = _("A processing activity must have a descriptive name.")
        err_1 = _(
            "A processing activity must either be new or already in place with changes required."
        )
        err_2 = _(
            "A processing activity can either be new or already in place with changes required, but not both or neither."
        )
        err_3 = _("A new processing activity must have a date of introduction.")
        err_4 = _("A changed processing activity must have a date of change.")
        if not self.cleaned_data.get("name"):
            raise forms.ValidationError(err_0)
        if (
            self.cleaned_data.get("is_new") is None
            and self.cleaned_data.get("has_changed") is None
        ):
            raise forms.ValidationError(err_1)
        if (
            self.cleaned_data.get("is_new") is True
            and self.cleaned_data.get("has_changed") is True
        ):
            raise forms.ValidationError(err_2)
        if (
            self.cleaned_data.get("is_new") is False
            and self.cleaned_data.get("has_changed") is False
        ):
            raise forms.ValidationError(err_2)
        if (
            self.cleaned_data.get("is_new") is None
            and self.cleaned_data.get("has_changed") is False
        ):
            raise forms.ValidationError(err_2)
        if (
            self.cleaned_data.get("is_new") is False
            and self.cleaned_data.get("has_changed") is None
        ):
            raise forms.ValidationError(err_2)
        if self.cleaned_data.get("is_new") is True and not self.cleaned_data.get(
            "date_intro"
        ):
            raise forms.ValidationError(err_3)
        if self.cleaned_data.get("has_changed") is True and not self.cleaned_data.get(
            "date_changed"
        ):
            raise forms.ValidationError(err_4)


class DataControllerForm(ModelForm):
    class Meta:
        model = DataController
        fields = [
            "dcon_name",
            "dcon_repby",
            "dcon_street",
            "dcon_pcode",
            "dcon_city",
            "dcon_country",
            "dcon_phone",
            "dcon_email",
            "dcon_web",
        ]
        labels = {
            "dcon_name": _("Data controller name:"),
            "dcon_repby": _("Data controller represented by:"),
            "dcon_street": _("Data controller - street:"),
            "dcon_pcode": _("Data controller - postal code:"),
            "dcon_city": _("Data controller - city:"),
            "dcon_country": _("Data controller - country:"),
            "dcon_phone": _("Data controller - phone:"),
            "dcon_email": _("Data controller - Email:"),
            "dcon_web": _("Data controller - Web:"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["dcon_name"].widget.attrs["readonly"] = True
        self.fields["dcon_repby"].widget.attrs["readonly"] = True
        self.fields["dcon_street"].widget.attrs["readonly"] = True
        self.fields["dcon_pcode"].widget.attrs["readonly"] = True
        self.fields["dcon_city"].widget.attrs["readonly"] = True
        self.fields["dcon_country"].widget.attrs["readonly"] = True
        self.fields["dcon_phone"].widget.attrs["readonly"] = True
        self.fields["dcon_email"].widget.attrs["readonly"] = True
        self.fields["dcon_web"].widget.attrs["readonly"] = True
        self.helper.layout = Layout(
            Row(
                Column(
                    "dcon_name",
                    "dcon_repby",
                    "dcon_street",
                    "dcon_pcode",
                    "dcon_city",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "dcon_country",
                    "dcon_phone",
                    "dcon_email",
                    "dcon_web",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Submit("submit", _("Submit"), css_class="btn btn-primary"),
            ),
        )


class JointControllerForm(ModelForm):
    class Meta:
        model = JointController
        fields = [
            "jcon_exists",
            "jcon_name",
            "jcon_repby",
            "jcon_street",
            "jcon_pcode",
            "jcon_city",
            "jcon_country",
            "jcon_contact",
        ]
        labels = {
            "jcon_exists": _("Joint controller exists?"),
            "jcon_name": _("Joint controller name:"),
            "jcon_repby": _("Joint controller represented by:"),
            "jcon_street": _("Joint controller - street:"),
            "jcon_pcode": _("Joint controller - postal code:"),
            "jcon_city": _("Joint controller - city:"),
            "jcon_country": _("Joint controller - country:"),
            "jcon_contact": _("Joint controller - contact person or department:"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row("jcon_exists", css_class="form-group col-md-6 mb-0"),
            Row(
                Column(
                    "jcon_name",
                    "jcon_repby",
                    "jcon_street",
                    "jcon_pcode",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "jcon_city",
                    "jcon_country",
                    "jcon_contact",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Submit("submit", _("Submit"), css_class="btn btn-primary"),
            ),
        )

    def clean(self):
        err_0 = _('Is there a joint controller? Choose either "Yes" or "No".')
        err_1 = _("If there is a joint controller, please enter their contact data.")
        if self.cleaned_data.get("jcon_exists") is None:
            raise forms.ValidationError(err_0)
        if self.cleaned_data.get("jcon_exists") is True and not self.cleaned_data.get(
            "jcon_name"
        ):
            raise forms.ValidationError(err_1)


class DataProtectionOfficerForm(ModelForm):
    class Meta:
        model = DataProtectionOfficer
        fields = [
            "dpo_name",
            "dpo_street",
            "dpo_pcode",
            "dpo_city",
            "dpo_country",
            "dpo_phone",
            "dpo_email",
            "dpo_web",
        ]
        labels = {
            "dpo_name": _("DPO name:"),
            "dpo_street": _("DPO street:"),
            "dpo_pcode": _("DPO postal code:"),
            "dpo_city": _("DPO city:"),
            "dpo_country": _("DPO country:"),
            "dpo_phone": _("DPO phone:"),
            "dpo_email": _("DPO Email:"),
            "dpo_web": _("DPO Web:"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["dpo_name"].widget.attrs["readonly"] = True
        self.fields["dpo_street"].widget.attrs["readonly"] = True
        self.fields["dpo_pcode"].widget.attrs["readonly"] = True
        self.fields["dpo_city"].widget.attrs["readonly"] = True
        self.fields["dpo_country"].widget.attrs["readonly"] = True
        self.fields["dpo_phone"].widget.attrs["readonly"] = True
        self.fields["dpo_email"].widget.attrs["readonly"] = True
        self.fields["dpo_web"].widget.attrs["readonly"] = True
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    "dpo_name",
                    "dpo_street",
                    "dpo_pcode",
                    "dpo_city",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "dpo_country",
                    "dpo_phone",
                    "dpo_email",
                    "dpo_web",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Submit("submit", _("Submit"), css_class="btn btn-primary"),
            ),
        )


class InternallyResponsibleDeptForm(ModelForm):
    email_regex = (
        "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.-]*" + settings.CONTROLLER_MAILDOM + "$"
    )
    ird_email = forms.EmailField(
        validators=[
            RegexValidator(
                regex=email_regex, message=_("Please enter a valid Email address.")
            )
        ],
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "placeholder": _("Must end on ") + settings.CONTROLLER_MAILDOM,
            }
        ),
        label=_("Internally responsible dept. Email:"),
    )

    class Meta:
        model = InternallyResponsibleDept
        fields = [
            "ird_name",
            "ird_street",
            "ird_pcode",
            "ird_city",
            "ird_country",
            "ird_phone",
            "ird_email",
            "ird_comments",
        ]
        labels = {
            "ird_name": _("Internally responsible dept. name:"),
            "ird_street": _("Internally responsible dept. street:"),
            "ird_pcode": _("Internally responsible dept. postal code:"),
            "ird_city": _("Internally responsible dept. city:"),
            "ird_country": _("Internally responsible dept. country:"),
            "ird_phone": _("Internally responsible dept. phone:"),
            "ird_comments": _("Internally responsible dept. comments:"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    "ird_name",
                    "ird_street",
                    "ird_pcode",
                    "ird_city",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "ird_country",
                    "ird_phone",
                    "ird_email",
                    "ird_comments",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Submit("submit", _("Submit"), css_class="btn btn-primary"),
            ),
        )


class CategoryOfPersonalDataFormSet(BaseModelFormSet):
    class Meta:
        model = CategoryOfPersonalData

    def clean(self):
        err_0 = _("Index already in use.")
        err_1 = _("Category of personal data missing.")
        indices_in_use = []
        for form in self.forms:
            if form.cleaned_data:
                index = form.cleaned_data.get("cpd_index")
                if index in indices_in_use:
                    form.add_error("cpd_index", err_0)
                else:
                    indices_in_use.append(index)
                if form.cleaned_data.get("cpd_index") and not form.cleaned_data.get(
                    "cpd_name"
                ):
                    form.add_error("cpd_name", err_1)


class CategoryOfPersonalDataForm(ModelForm):
    class Meta:
        model = CategoryOfPersonalData
        fields = ["cpd_index", "cpd_name", "cpd_is_special"]
        labels = {
            "cpd_index": _("Index no."),
            "cpd_name": _("Category of personal data"),
            "cpd_is_special": _("Special category"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", _("Submit"), css_class="btn-primary"))
        self.helper.form_method = "POST"
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Row(
                Column("cpd_index", css_class="form-group col-md-0 mb-0"),
                Column("cpd_name", css_class="form-group col-md-4 mb-0"),
                Column("cpd_is_special", css_class="form-group col-md-0 mb-0"),
                Column("DELETE", css_class="form-group col-md-0 mb-0"),
            ),
        )

    def clean(self):
        err_0 = _("At least one category of personal data is required.")
        if self.cleaned_data.get("cpd_index") is None:
            raise forms.ValidationError(err_0)


class CpdModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.cpd_name


class CategoriesOfPersonalDataOriginForm(ModelForm):
    class Meta:
        model = CategoriesOfPersonalDataOrigin
        fields = ["cpdo_descr"]
        widgets = {
            "cpdo_descr": Textarea(attrs={"cols": 80, "rows": 10}),
        }
        labels = {
            "cpdo_descr": _("Categories of personal data origin:"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    "cpdo_descr",
                    css_class="form-group col-md-10 mb-0",
                ),
            ),
            Row(
                Submit("submit", _("Submit"), css_class="btn btn-primary"),
            ),
        )

    def clean(self):
        err_0 = _(
            "Please give a brief description of the origin of the personal data to be processed."
        )
        if not self.cleaned_data.get("cpdo_descr"):
            raise forms.ValidationError(err_0)


class PurposeAndLegalBasisForm(ModelForm):
    class Meta:
        model = PurposeAndLegalBasis
        fields = ["plb_purpose", "plb", "plb_reasons"]
        widgets = {
            "plb_purpose": Textarea(attrs={"cols": 80, "rows": 10}),
            "plb_reasons": Textarea(attrs={"cols": 80, "rows": 10}),
        }
        labels = {
            "plb_purpose": _("Purpose of processing activity:"),
            "plb": _(
                "Exhaustive list of legal bases (at least one is strictly required):"
            ),
            "plb_reasons": _("Explanation for choice of legal bases:"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    "plb_purpose",
                    "plb",
                    "plb_reasons",
                    css_class="form-group col-md-10 mb-0",
                ),
            ),
            Row(
                Submit("submit", _("Submit"), css_class="btn btn-primary"),
            ),
        )


class DataSubjectForm(ModelForm):
    class Meta:
        model = DataSubject
        fields = ["dsub_name", "dsub_cpd_sel"]
        labels = {
            "dsub_name": _("Data subject category name:"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", _("Submit"), css_class="btn-primary"))
        self.helper.form_method = "POST"
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Row(
                Column("dsub_name", css_class="form-group col-md-4 mb-0"),
                Column("dsub_cpd_sel", css_class="form-group col-md-0 mb-0"),
                Column("DELETE", css_class="form-group col-md-0 mb-0"),
            ),
            HTML(
                '{% if forloop.counter < 9 %} <hr class="formset-divider"> {% endif %}'
            ),
        )

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            instance.cpd.clear()
            for cpd in self.cleaned_data.get("dsub_cpd_sel"):
                instance.cpd.add(cpd)

        self.save_m2m = save_m2m
        instance.save()
        self.save_m2m()
        return instance

    def clean(self):
        err_0 = _(
            "At least one data subject category is required (otherwise you would not process personal data)."
        )
        err_1 = _(
            "You must fill in the categories of personal data for this data subject category."
        )

        if not self.cleaned_data.get("dsub_name"):
            raise forms.ValidationError(err_0, code="no_dsub")
        if not self.cleaned_data.get("dsub_cpd_sel"):
            raise forms.ValidationError(err_1, code="no_dsub_cpd_given")


class TimeLimitForErasureFormSet(BaseModelFormSet):
    class Meta:
        model = TimeLimitForErasure

    def clean(self):
        super().clean()
        err_0 = _(
            "Time limits for erasure handling: Select how to state your time limits for erasure."
        )
        err_1 = _("At least one time limit for erasure (start and length) is required.")
        err_2 = _("Please state a reason for this time limit for erasure.")
        err_3 = _(
            "You must fill in the categories of personal data for this time limit for erasure."
        )
        for form in self.forms:
            if form.cleaned_data:
                tle_handling_flag = form.cleaned_data.get("tle_handling")
                break
        if not tle_handling_flag:
            form.add_error("tle_handling", err_0)
        # set tle_handling for forms with valid data but without field for tle_handling
        # https://docs.djangoproject.com/en/4.1/topics/forms/modelforms/#overriding-clean-on-a-modelformset
        for form in self.forms:
            if form.cleaned_data:
                if not form.cleaned_data.get("tle_handling"):
                    form.cleaned_data["tle_handling"] = tle_handling_flag
                    form.instance.tle_handling = tle_handling_flag
        # actual validation for TLE in RPA
        if tle_handling_flag == "tle_in_rpa":
            for form in self.forms:
                if form.cleaned_data:
                    if not form.cleaned_data.get("tle_start"):
                        form.add_error("tle_start", err_1)
                    if not form.cleaned_data.get("tle_length"):
                        form.add_error("tle_length", err_1)
                    if not form.cleaned_data.get("tle_comment"):
                        form.add_error("tle_comment", err_2)
                    if not form.cleaned_data.get("tle_cpd_sel"):
                        form.add_error("tle_cpd_sel", err_3)


class TimeLimitForErasureForm(ModelForm):
    class Meta:
        model = TimeLimitForErasure
        fields = [
            "tle_handling",
            "tle_start",
            "tle_length",
            "tle_comment",
            "tle_cpd_sel",
        ]
        labels = {
            "tle_handling": _(
                "How do you want to add time limits for erasure to your RPA?"
            ),
            "tle_start": _("Timelimit for erasure start:"),
            "tle_length": _("Timelimit for erasure length:"),
            "tle_comment": _("Timelimit for erasure comment:"),
        }
        widgets = {
            "tle_comment": Textarea(attrs={"cols": 50, "rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper_first = FormHelper()
        self.helper_first.form_tag = False
        self.helper_first.disable_csrf = True
        self.helper_first.render_hidden_fields = True
        self.helper_first.layout = Layout(
            Row(
                Column("tle_handling", css_class="form-group col-md-7 mb-0"),
            ),
            HTML('<hr class="formset-divider">'),
            Row(
                Column("tle_start", css_class="form-group col-md-2 mb-0"),
                Column("tle_length", css_class="form-group col-md-2 mb-0"),
                Column("tle_cpd_sel", css_class="form-group col-md-0 mb-0"),
                Column("DELETE", css_class="form-group col-md-1 mb-0"),
            ),
            Row(
                Column("tle_comment", css_class="form-group col-md-4 mb-0"),
            ),
            HTML('<hr class="formset-divider">'),
        )
        self.helper_between = FormHelper()
        self.helper_between.form_tag = False
        self.helper_between.disable_csrf = True
        self.helper_between.render_hidden_fields = True
        self.helper_between.layout = Layout(
            Row(
                Column("tle_start", css_class="form-group col-md-2 mb-0"),
                Column("tle_length", css_class="form-group col-md-2 mb-0"),
                Column("tle_cpd_sel", css_class="form-group col-md-0 mb-0"),
                Column("DELETE", css_class="form-group col-md-1 mb-0"),
            ),
            Row(
                Column("tle_comment", css_class="form-group col-md-4 mb-0"),
            ),
            HTML('<hr class="formset-divider">'),
        )
        self.helper_last = FormHelper()
        self.helper_last.add_input(
            Submit("submit", _("Submit"), css_class="btn-primary")
        )
        self.helper_last.form_tag = False
        self.helper_last.disable_csrf = True
        self.helper_last.render_hidden_fields = True
        self.helper_last.layout = Layout(
            Row(
                Column("tle_start", css_class="form-group col-md-2 mb-0"),
                Column("tle_length", css_class="form-group col-md-2 mb-0"),
                Column("tle_cpd_sel", css_class="form-group col-md-0 mb-0"),
                Column("DELETE", css_class="form-group col-md-1 mb-0"),
            ),
            Row(
                Column("tle_comment", css_class="form-group col-md-4 mb-0"),
            ),
        )

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            instance.cpd.clear()
            for cpd in self.cleaned_data.get("tle_cpd_sel"):
                instance.cpd.add(cpd)

        self.save_m2m = save_m2m
        instance.save()
        self.save_m2m()
        return instance


class CategoryOfRecipientsFormSet(BaseModelFormSet):
    class Meta:
        model = CategoryOfRecipients

    def clean(self):
        super().clean()
        err_0 = _(
            "Are there categories of recipients, i.e. do you intend to transfer personal data to some person or entity (both internal or external, but inside the ambit of the GDPR)? Choose the appropriate option."
        )
        err_1 = _(
            "If you intend to transfer personal data, you must fill in the recipients."
        )
        err_2 = _(
            'Is this recipient an external recipient? Choose either "Yes" or "No".'
        )
        err_3 = _(
            "If you intend to transfer personal data, you must fill in the affected categories of personal data."
        )
        for form in self.forms:
            if form.cleaned_data:
                crec_handling_flag = form.cleaned_data.get("crec_handling")
                break
        if not crec_handling_flag:
            form.add_error("crec_handling", err_0)
        # set crec_handling for forms with valid data but without field for crec_handling
        for form in self.forms:
            if form.cleaned_data:
                if not form.cleaned_data.get("crec_handling"):
                    form.cleaned_data["crec_handling"] = crec_handling_flag
                    form.instance.crec_handling = crec_handling_flag
        # actual validation for CRec in RPA
        if crec_handling_flag == "crec_in_rpa":
            for form in self.forms:
                if form.cleaned_data:
                    if not form.cleaned_data.get("crec_designation"):
                        form.add_error("crec_designation", err_1)
                    if form.cleaned_data.get("crec_is_external") is None:
                        form.add_error("crec_is_external", err_2)
                    if not form.cleaned_data.get("crec_cpd_sel"):
                        form.add_error("crec_cpd_sel", err_3)


class CategoryOfRecipientsForm(ModelForm):
    class Meta:
        model = CategoryOfRecipients
        fields = [
            "crec_handling",
            "crec_designation",
            "crec_is_external",
            "crec_cpd_sel",
        ]
        labels = {
            "crec_handling": _(
                "Are there categories of recipients? If yes, how do you want to add information regarding these to your RPA?"
            ),
            "crec_designation": _("Category of recipients designation:"),
            "crec_is_external": _("Is this category of recipients external?"),
        }
        widgets = {
            "crec_designation": Textarea(attrs={"cols": 50, "rows": 8}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper_first = FormHelper()
        self.helper_first.form_tag = False
        self.helper_first.disable_csrf = True
        self.helper_first.render_hidden_fields = True
        self.helper_first.layout = Layout(
            Row(
                Column("crec_handling", css_class="form-group col-md-7 mb-0"),
            ),
            HTML('<hr class="formset-divider">'),
            Row(
                Column("crec_designation", css_class="form-group col-md-5 mb-0"),
                Column("crec_is_external", css_class="form-group col-md-2 mb-0"),
            ),
            Row(
                Column("crec_cpd_sel", css_class="form-group col-md-6 mb-0"),
                Column("DELETE", css_class="form-group col-md-1 mb-0"),
            ),
            HTML('<hr class="formset-divider">'),
        )
        self.helper_between = FormHelper()
        self.helper_between.form_tag = False
        self.helper_between.disable_csrf = True
        self.helper_between.render_hidden_fields = True
        self.helper_between.layout = Layout(
            Row(
                Column("crec_designation", css_class="form-group col-md-5 mb-0"),
                Column("crec_is_external", css_class="form-group col-md-2 mb-0"),
            ),
            Row(
                Column("crec_cpd_sel", css_class="form-group col-md-6 mb-0"),
                Column("DELETE", css_class="form-group col-md-1 mb-0"),
            ),
            HTML('<hr class="formset-divider">'),
        )
        self.helper_last = FormHelper()
        self.helper_last.add_input(
            Submit("submit", _("Submit"), css_class="btn-primary")
        )
        self.helper_last.form_tag = False
        self.helper_last.disable_csrf = True
        self.helper_last.render_hidden_fields = True
        self.helper_last.layout = Layout(
            Row(
                Column("crec_designation", css_class="form-group col-md-5 mb-0"),
                Column("crec_is_external", css_class="form-group col-md-2 mb-0"),
            ),
            Row(
                Column("crec_cpd_sel", css_class="form-group col-md-6 mb-0"),
                Column("DELETE", css_class="form-group col-md-1 mb-0"),
            ),
        )

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            instance.cpd.clear()
            for cpd in self.cleaned_data.get("crec_cpd_sel"):
                instance.cpd.add(cpd)

        self.save_m2m = save_m2m
        instance.save()
        self.save_m2m()
        return instance


class TransferToThirdCountryForm(ModelForm):
    class Meta:
        model = TransferToThirdCountry
        fields = [
            "ttc_3rdcountry_intended",
            "ttc_3rdcountry",
            "ttc_3rdcountry_adequacy",
            "ttc_non_adequacy_choices",
            "ttc_non_adequacy_explanation",
        ]
        labels = {
            "ttc_3rdcountry_intended": _(
                "Do you intend to transfer data to a 3rd country or int. org.?"
            ),
            "ttc_3rdcountry": _("3rd country or int. org. recipients designation:"),
            "ttc_3rdcountry_adequacy": _(
                "Is there an adequacy decision for this transfer?"
            ),
            "ttc_non_adequacy_choices": _(
                "Choose the applicable exception for non-adequacy transfer:"
            ),
            "ttc_non_adequacy_explanation": _("Explanation for choice of exception:"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("ttc_3rdcountry_intended", css_class="form-group col-md-4 mb-0"),
            ),
            Row(
                Column(
                    "ttc_3rdcountry",
                    "ttc_3rdcountry_adequacy",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Column(
                    "ttc_non_adequacy_choices",
                    "ttc_non_adequacy_explanation",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Submit("submit", _("Submit"), css_class="btn btn-primary"),
            ),
        )

    def clean(self):
        err_0 = _(
            'Do you intend to transfer personal data to a third country or an international organisation? Choose either "Yes" or "No".'
        )
        err_1 = _(
            "If you intend to transfer personal data to a third country or an international organisation, you must fill in the recipients (can be one or more)."
        )
        err_2 = _(
            'Is there an adequacy decision for your intended transfer? Choose either "Yes" or "No".'
        )
        err_3 = _(
            "If there is no adequacy decision, you must choose at least one exception that applies for your intended transfer."
        )
        err_4 = _(
            "Please explain the exception you chose for your intended transfer without adequacy decision. If in doubt, contact the DPO."
        )
        if self.cleaned_data.get("ttc_3rdcountry_intended") is None:
            raise forms.ValidationError(err_0, code="ttc_undecided")
        if self.cleaned_data.get("ttc_3rdcountry_intended") is True:
            if self.cleaned_data.get(
                "ttc_3rdcountry_intended"
            ) is True and not self.cleaned_data.get("ttc_3rdcountry"):
                raise forms.ValidationError(err_1, code="no_ttc_given")
            if self.cleaned_data.get("ttc_3rdcountry_adequacy") is None:
                raise forms.ValidationError(err_2, code="no_ttc_adequacy")
            if (self.cleaned_data.get("ttc_3rdcountry_adequacy") is False) and (
                len(self.cleaned_data.get("ttc_non_adequacy_choices")) < 1
            ):
                raise forms.ValidationError(err_3, code="no_ttc_adequacy_choice")
            if (self.cleaned_data.get("ttc_3rdcountry_adequacy") is False) and (
                len(self.cleaned_data.get("ttc_non_adequacy_choices")) >= 1
            ):
                if not self.cleaned_data.get("ttc_non_adequacy_explanation"):
                    raise forms.ValidationError(
                        err_4, code="no_ttc_non_adequacy_explanation"
                    )


class AccessGroupFormSet(BaseModelFormSet):
    class Meta:
        model = AccessGroup

    def clean(self):
        super().clean()
        err_0 = _(
            "Access group handling: Select how to state access groups for this RPA."
        )
        err_1 = _("At least one access group must be named.")
        err_2 = _(
            'Access rights - "Read", "Edit" and "Delete" - for this access group must each be either "Yes" or "No".'
        )
        err_3 = _("An access group with no access rights does not make sense.")
        err_4 = _(
            "You must fill in the categories of personal data this access group has access to."
        )
        for form in self.forms:
            if form.cleaned_data:
                agrp_handling_flag = form.cleaned_data.get("agrp_handling")
                break
        if not agrp_handling_flag:
            form.add_error("agrp_handling", err_0)
        # set agrp_handling for forms with valid data but without field for agrp_handling
        for form in self.forms:
            if form.cleaned_data:
                if not form.cleaned_data.get("agrp_handling"):
                    form.cleaned_data["agrp_handling"] = agrp_handling_flag
                    form.instance.agrp_handling = agrp_handling_flag
        # actual validation for AGrp in RPA
        if agrp_handling_flag == "agrp_in_rpa":
            for form in self.forms:
                if form.cleaned_data:
                    if not form.cleaned_data.get("agrp_name"):
                        form.add_error("agrp_name", err_1)
                    if form.cleaned_data.get("agrp_can_read") is None:
                        form.add_error("agrp_can_read", err_2)
                    if form.cleaned_data.get("agrp_can_edit") is None:
                        form.add_error("agrp_can_edit", err_2)
                    if form.cleaned_data.get("agrp_can_delete") is None:
                        form.add_error("agrp_can_delete", err_2)
                    if (
                        form.cleaned_data.get("agrp_can_read") is False
                        and form.cleaned_data.get("agrp_can_edit") is False
                        and form.cleaned_data.get("agrp_can_delete") is False
                    ):
                        form.add_error("agrp_can_read", err_3)
                        form.add_error("agrp_can_edit", err_3)
                        form.add_error("agrp_can_delete", err_3)
                    if not form.cleaned_data.get("agrp_cpd_sel"):
                        form.add_error("agrp_cpd_sel", err_4)


class AccessGroupForm(ModelForm):
    class Meta:
        model = AccessGroup
        fields = [
            "agrp_handling",
            "agrp_name",
            "agrp_can_read",
            "agrp_can_edit",
            "agrp_can_delete",
            "agrp_cpd_sel",
        ]
        labels = {
            "agrp_handling": _("How do you want to add access groups to your RPA?"),
            "agrp_name": _("Access group designation:"),
            "agrp_can_read": _("Can read"),
            "agrp_can_edit": _("Can edit"),
            "agrp_can_delete": _("Can delete"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper_first = FormHelper()
        self.helper_first.form_tag = False
        self.helper_first.disable_csrf = True
        self.helper_first.render_hidden_fields = True
        self.helper_first.layout = Layout(
            Row(
                Column("agrp_handling", css_class="form-group col-md-7 mb-0"),
            ),
            HTML('<hr class="formset-divider">'),
            Row(
                Column("agrp_name", css_class="form-group col-md-6 mb-0"),
                Column("agrp_cpd_sel", css_class="form-group col-md-4 mb-0"),
                Column("DELETE", css_class="form-group col-md-0 mb-0"),
            ),
            Row(
                Column("agrp_can_read", css_class="form-group col-md-2 mb-0"),
                Column("agrp_can_edit", css_class="form-group col-md-2 mb-0"),
                Column("agrp_can_delete", css_class="form-group col-md-2 mb-0"),
            ),
            HTML('<hr class="formset-divider">'),
        )
        self.helper_between = FormHelper()
        self.helper_between.form_tag = False
        self.helper_between.disable_csrf = True
        self.helper_between.render_hidden_fields = True
        self.helper_between.layout = Layout(
            Row(
                Column("agrp_name", css_class="form-group col-md-6 mb-0"),
                Column("agrp_cpd_sel", css_class="form-group col-md-4 mb-0"),
                Column("DELETE", css_class="form-group col-md-0 mb-0"),
            ),
            Row(
                Column("agrp_can_read", css_class="form-group col-md-2 mb-0"),
                Column("agrp_can_edit", css_class="form-group col-md-2 mb-0"),
                Column("agrp_can_delete", css_class="form-group col-md-2 mb-0"),
            ),
            HTML('<hr class="formset-divider">'),
        )
        self.helper_last = FormHelper()
        self.helper_last.add_input(
            Submit("submit", _("Submit"), css_class="btn-primary")
        )
        self.helper_last.form_tag = False
        self.helper_last.disable_csrf = True
        self.helper_last.render_hidden_fields = True
        self.helper_last.layout = Layout(
            Row(
                Column("agrp_name", css_class="form-group col-md-6 mb-0"),
                Column("agrp_cpd_sel", css_class="form-group col-md-4 mb-0"),
                Column("DELETE", css_class="form-group col-md-0 mb-0"),
            ),
            Row(
                Column("agrp_can_read", css_class="form-group col-md-2 mb-0"),
                Column("agrp_can_edit", css_class="form-group col-md-2 mb-0"),
                Column("agrp_can_delete", css_class="form-group col-md-2 mb-0"),
            ),
        )

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            instance.cpd.clear()
            for cpd in self.cleaned_data.get("agrp_cpd_sel"):
                instance.cpd.add(cpd)

        self.save_m2m = save_m2m
        instance.save()
        self.save_m2m()
        return instance


class TransparencyForm(ModelForm):
    class Meta:
        model = Transparency
        fields = ["tran_choices", "tran_explanation"]
        labels = {
            "tran_choices": _(
                "Select the intended method to inform the data subjects:"
            ),
            "tran_explanation": _("State the details for the information method:"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    "tran_choices",
                    "tran_explanation",
                    css_class="form-group col-md-10 mb-0",
                ),
            ),
            Row(
                Submit("submit", _("Submit"), css_class="btn btn-primary"),
            ),
        )

    def clean(self):
        err_0 = _("You must choose at least one way to inform the data subjects.")
        err_1 = _("Please provide at least one reference to your information.")
        if not self.cleaned_data.get("tran_choices"):
            raise forms.ValidationError(err_0, code="no_tran")
        if not self.cleaned_data.get("tran_explanation"):
            raise forms.ValidationError(err_1, code="no_tran_ref")


class DataProcessorForm(ModelForm):
    class Meta:
        model = DataProcessor
        fields = [
            "dpro_is_assigned",
            "dpro_name",
            "dpro_street",
            "dpro_pcode",
            "dpro_city",
            "dpro_country",
            "dpro_contact",
        ]
        labels = {
            "dpro_is_assigned": _(
                "Is a data processor assigned for your processing activity?"
            ),
            "dpro_name": _("Data processor name:"),
            "dpro_street": _("Data processor street:"),
            "dpro_pcode": _("Data processor postal code:"),
            "dpro_city": _("Data processor city:"),
            "dpro_country": _("Data processor country:"),
            "dpro_contact": _("Data processor contact person (optional):"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row("dpro_is_assigned", css_class="form-group col-md-6 mb-0"),
            Row(
                Column(
                    "dpro_name",
                    "dpro_street",
                    "dpro_pcode",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "dpro_city",
                    "dpro_country",
                    "dpro_contact",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Submit("submit", _("Submit"), css_class="btn btn-primary"),
            ),
        )

    def clean(self):
        err_0 = _('Is there a data processor? Choose either "Yes" or "No".')
        err_1 = _("If there is a data processor, please enter their contact data.")
        if self.cleaned_data.get("dpro_is_assigned") is None:
            raise forms.ValidationError(err_0, code="no_dpro")
        if self.cleaned_data.get(
            "dpro_is_assigned"
        ) is True and not self.cleaned_data.get("dpro_name"):
            raise forms.ValidationError(err_1, code="no_dpro_name")


class PrivacyImpactAssessmentForm(ModelForm):
    class Meta:
        model = PrivacyImpactAssessment
        fields = [
            "pia_required",
            "pia_not_required_reason",
            "pia_results",
        ]
        labels = {
            "pia_required": _("Does your processing activity require a PIA/DPIA?"),
            "pia_not_required_reason": _(
                "State the reasons for a PIA not being required:"
            ),
            "pia_results": _("PIA results:"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row("pia_required"),
            Row("pia_not_required_reason"),
            Row("pia_results"),
            Row(
                Submit("submit", _("Submit"), css_class="btn btn-primary"),
            ),
        )

    def clean(self):
        err_0 = _(
            'Is a privacy impact assessment required for your processing activity? Choose either "Yes" or "No".'
        )
        err_1 = _(
            "Read and check all circumstances that must not be present in order for a PIA not being required."
        )
        err_2 = _("A PIA must have one single result.")
        if self.cleaned_data.get("pia_required") is None:
            raise forms.ValidationError(err_0, code="no_pia")
        if self.cleaned_data.get("pia_required") is False and not self.cleaned_data.get(
            "pia_not_required_reason"
        ):
            raise forms.ValidationError(err_1, code="no_pia_nr_reason")
        if (
            self.cleaned_data.get("pia_required") is False
            and len(self.cleaned_data.get("pia_not_required_reason")) != 4
        ):
            raise forms.ValidationError(err_1, code="no_pia_nr_reason")
        if (
            self.cleaned_data.get("pia_required") is True
            and len(self.cleaned_data.get("pia_results")) != 1
        ):
            raise forms.ValidationError(err_2, code="no_pia_result")


class TOMForm(ModelForm):
    class Meta:
        model = TOM
        fields = [
            "tom_handling",
            "tom_pseudonym_selection",
            "tom_pseudonym",
            "tom_encryption_selection",
            "tom_encryption",
            "tom_integrity_selection",
            "tom_integrity",
            "tom_availability_selection",
            "tom_availability",
            "tom_evaluation_selection",
            "tom_evaluation",
            "tom_appropriation_selection",
            "tom_appropriation",
            "tom_transparency_selection",
            "tom_transparency",
            "tom_subject_rights_selection",
            "tom_subject_rights",
        ]
        labels = {
            "tom_handling": _("How do you want to add the TOM to your RPA?"),
            "tom_pseudonym_selection": _(
                "Select measures regarding pseudonymization that apply:"
            ),
            "tom_pseudonym": _(
                "Describe other or further measures regarding pseudonymization that apply:"
            ),
            "tom_encryption_selection": _(
                "Select measures regarding encryption that apply:"
            ),
            "tom_encryption": _(
                "Describe other or further measures regarding encryption that apply:"
            ),
            "tom_integrity_selection": _(
                "Select measures regarding integrity/confidentiality that apply:"
            ),
            "tom_integrity": _(
                "Describe other or further measures regarding integrity/confidentiality that apply:"
            ),
            "tom_availability_selection": _(
                "Select measures regarding availability/resilience that apply:"
            ),
            "tom_availability": _(
                "Describe other or further measures regarding availability/resilience that apply:"
            ),
            "tom_evaluation_selection": _(
                "Select measures regarding evaluation that apply:"
            ),
            "tom_evaluation": _(
                "Describe other or further measures regarding evaluation that apply:"
            ),
            "tom_appropriation_selection": _(
                "Select measures regarding appropriation that apply:"
            ),
            "tom_appropriation": _(
                "Describe other or further measures regarding appropriation that apply:"
            ),
            "tom_transparency_selection": _(
                "Select measures regarding transparency that apply:"
            ),
            "tom_transparency": _(
                "Describe other or further measures regarding transparency that apply:"
            ),
            "tom_subject_rights_selection": _(
                "Select measures regarding subject rights that apply:"
            ),
            "tom_subject_rights": _(
                "Describe other or further measures regarding subject rights that apply:"
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column("tom_handling", css_class="form-group col-md-8 mb-0")),
            Row(
                Column("tom_pseudonym_selection", css_class="form-group col-md-8 mb-0")
            ),
            Row(Column("tom_pseudonym", css_class="form-group col-md-8 mb-0")),
            HTML('<hr class="tom-divider">'),
            Row(
                Column("tom_encryption_selection", css_class="form-group col-md-8 mb-0")
            ),
            Row(Column("tom_encryption", css_class="form-group col-md-8 mb-0")),
            HTML('<hr class="tom-divider">'),
            Row(
                Column("tom_integrity_selection", css_class="form-group col-md-8 mb-0")
            ),
            Row(Column("tom_integrity", css_class="form-group col-md-8 mb-0")),
            HTML('<hr class="tom-divider">'),
            Row(
                Column(
                    "tom_availability_selection", css_class="form-group col-md-8 mb-0"
                )
            ),
            Row(Column("tom_availability", css_class="form-group col-md-8 mb-0")),
            HTML('<hr class="tom-divider">'),
            Row(
                Column("tom_evaluation_selection", css_class="form-group col-md-8 mb-0")
            ),
            Row(Column("tom_evaluation", css_class="form-group col-md-8 mb-0")),
            HTML('<hr class="tom-divider">'),
            Row(
                Column(
                    "tom_appropriation_selection", css_class="form-group col-md-8 mb-0"
                )
            ),
            Row(Column("tom_appropriation", css_class="form-group col-md-8 mb-0")),
            HTML('<hr class="tom-divider">'),
            Row(
                Column(
                    "tom_transparency_selection", css_class="form-group col-md-8 mb-0"
                )
            ),
            Row(Column("tom_transparency", css_class="form-group col-md-8 mb-0")),
            HTML('<hr class="tom-divider">'),
            Row(
                Column(
                    "tom_subject_rights_selection", css_class="form-group col-md-8 mb-0"
                )
            ),
            Row(Column("tom_subject_rights", css_class="form-group col-md-8 mb-0")),
            Row(
                Submit("submit", _("Submit"), css_class="btn btn-primary"),
            ),
        )

    def clean(self):
        err_0 = _("TOM handling: Select how to state your TOM.")
        err_1 = _(
            'TOM Pseudonymization: Select/describe pseudonymization-related measures or choose the "purpose does not allow pseudonymization" option.'
        )
        err_2 = _("TOM Encryption: Select/describe encryption-related measures.")
        err_3 = _(
            "TOM Integrity: Select/describe integrity- and confidentiality-related measures."
        )
        err_4 = _(
            "TOM Availability: Select/describe availability- and resilience-related measures."
        )
        err_5 = _("TOM Evaluation: Select/describe evaluation-related measures.")
        err_6 = _("TOM Appropriation: Select/describe appropriation-related measures.")
        err_7 = _("TOM Transparency: Select/describe transparency-related measures.")
        err_8 = _(
            "TOM Subject rights: Select/describe subject rights-related measures."
        )
        if self.cleaned_data.get("tom_handling") == "":
            raise forms.ValidationError(err_0, code="no_tom_handling")
        if self.cleaned_data.get("tom_handling") == "tom_in_rpa":
            if not self.cleaned_data.get(
                "tom_pseudonym_selection"
            ) and not self.cleaned_data.get("tom_pseudonym"):
                raise forms.ValidationError(err_1, code="no_tom_pseudonym")
            if not self.cleaned_data.get(
                "tom_encryption_selection"
            ) and not self.cleaned_data.get("tom_encryption"):
                raise forms.ValidationError(err_2, code="no_tom_encryption")
            if not self.cleaned_data.get(
                "tom_integrity_selection"
            ) and not self.cleaned_data.get("tom_integrity"):
                raise forms.ValidationError(err_3, code="no_tom_integrity")
            if not self.cleaned_data.get(
                "tom_availability_selection"
            ) and not self.cleaned_data.get("tom_availability"):
                raise forms.ValidationError(err_4, code="no_tom_availability")
            if not self.cleaned_data.get(
                "tom_evaluation_selection"
            ) and not self.cleaned_data.get("tom_evaluation"):
                raise forms.ValidationError(err_5, code="no_tom_evaluation")
            if not self.cleaned_data.get(
                "tom_appropriation_selection"
            ) and not self.cleaned_data.get("tom_appropriation"):
                raise forms.ValidationError(err_6, code="no_tom_appropriation")
            if not self.cleaned_data.get(
                "tom_transparency_selection"
            ) and not self.cleaned_data.get("tom_transparency"):
                raise forms.ValidationError(err_7, code="no_tom_transparency")
            if not self.cleaned_data.get(
                "tom_subject_rights_selection"
            ) and not self.cleaned_data.get("tom_subject_rights"):
                raise forms.ValidationError(err_8, code="no_tom_subject_rights")


class RPAAnnexFormSet(BaseModelFormSet):
    class Meta:
        model = RPAAnnex

    def clean(self):
        err_0 = _("Index already in use.")
        err_1 = _("Annex entry missing.")
        indices_in_use = []
        for form in self.forms:
            if form.cleaned_data:
                index = form.cleaned_data.get("annex_index")
                if index in indices_in_use:
                    form.add_error("annex_index", err_0)
                else:
                    indices_in_use.append(index)
                if form.cleaned_data.get("annex_index") and not form.cleaned_data.get(
                    "annex_name"
                ):
                    form.add_error("annex_name", err_1)


class RPAAnnexForm(ModelForm):
    class Meta:
        model = RPAAnnex
        fields = ["annex_index", "annex_name"]
        labels = {
            "annex_index": _("Annex No."),
            "annex_name": _("Annex"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", _("Submit"), css_class="btn-primary"))
        self.helper.form_method = "POST"
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Row(
                Column("annex_index", css_class="form-group col-md-1 mb-0"),
                Column("annex_name", css_class="form-group col-md-8 mb-0"),
                Column("DELETE", css_class="form-group col-md-1 mb-0"),
            ),
        )

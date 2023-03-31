"""Breach reporter forms
All the form classes below are standard, textbook-like modelforms.
__init__() is overridden to allow crispy forms to kick in, clean() is
overridden to do custom form validation.
"""

from django import forms
from django.forms import ModelForm
from django.forms.widgets import NumberInput, Textarea, Select, RadioSelect
from django.core.validators import RegexValidator
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Field

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


class BreachForm(ModelForm):
    lowercase_only_regex = r"^[a-z0-9\_\-]+$"
    slug = forms.SlugField(
        min_length=8,
        max_length=20,
        label=_('Short name ("slug") for your breach notification:'),
        validators=[
            RegexValidator(
                regex=lowercase_only_regex,
                message=_(
                    "Please use lowercase letters, numbers, hyphens and underscores only."
                ),
            )
        ],
    )
    breach_bumper = forms.BooleanField(
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
        model = Breach
        fields = ["slug", "breach_bumper", "helptext_display_default"]
        labels = {
            "helptext_display_default": _("Boxes with help texts shall by default be"),
        }
        widgets = {
            "helptext_display_default": Select(choices=HELP_TEXT_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "edit-slug"
        self.helper.layout = Layout(
            Row(
                Column("slug", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("breach_bumper", css_class="form-group col-md-6 mb-0"),
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


class BreachDataControllerForm(ModelForm):
    class Meta:
        model = BreachDataController
        fields = [
            "dcon_name",
            "dcon_street",
            "dcon_pcode",
            "dcon_city",
            "dcon_email",
            "dcon_reporter",
            "dcon_reporter_function",
            "dcon_reporter_email",
            "dcon_reporter_phone",
            "dcon_dpo_name",
            "dcon_dpo_email",
            "dcon_dpo_phone",
            "dcon_dpo_comment",
        ]
        labels = {
            "dcon_name": _("Data controller - name:"),
            "dcon_street": _("Data controller - street:"),
            "dcon_pcode": _("Data controller - postal code:"),
            "dcon_city": _("Data controller - city:"),
            "dcon_email": _("Data controller - email address:"),
            "dcon_reporter": _("Reporting person's name:"),
            "dcon_reporter_function": _("Reporting person's function:"),
            "dcon_reporter_email": _("Reporting person's email address:"),
            "dcon_reporter_phone": _("Reporting person's phone number:"),
            "dcon_dpo_name": _("Data controller - DPO name:"),
            "dcon_dpo_email": _("Data controller - DPO email address:"),
            "dcon_dpo_phone": _("Data controller - DPO phone number:"),
            "dcon_dpo_comment": settings.DPO_COMMENT,
        }
        help_texts = {
            "dcon_dpo_comment": settings.DPO_COMMENT_HELPTEXT,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "edit-dcon"
        self.fields["dcon_name"].widget.attrs["readonly"] = True
        self.fields["dcon_street"].widget.attrs["readonly"] = True
        self.fields["dcon_pcode"].widget.attrs["readonly"] = True
        self.fields["dcon_city"].widget.attrs["readonly"] = True
        self.fields["dcon_email"].widget.attrs["readonly"] = True
        self.fields["dcon_reporter"].widget.attrs["readonly"] = True
        self.fields["dcon_reporter_function"].widget.attrs["readonly"] = True
        self.fields["dcon_reporter_email"].widget.attrs["readonly"] = True
        self.fields["dcon_reporter_phone"].widget.attrs["readonly"] = True
        self.fields["dcon_dpo_name"].widget.attrs["readonly"] = True
        self.fields["dcon_dpo_email"].widget.attrs["readonly"] = True
        self.fields["dcon_dpo_phone"].widget.attrs["readonly"] = True
        self.helper.layout = Layout(
            Row(
                Column(
                    "dcon_name",
                    "dcon_street",
                    "dcon_pcode",
                    "dcon_city",
                    "dcon_email",
                    "dcon_dpo_name",
                    "dcon_dpo_email",
                    "dcon_dpo_phone",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "dcon_reporter",
                    "dcon_reporter_function",
                    "dcon_reporter_email",
                    "dcon_reporter_phone",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Submit("submit", _("Submit"), css_class="btn btn-primary"),
            ),
        )


class BreachTimeLineForm(ModelForm):
    class Meta:
        model = BreachTimeLine
        fields = [
            "btl_start",
            "btl_start_known",
            "btl_end",
            "btl_ongoing",
            "btl_may_recur",
            "btl_noticed",
            "btl_notif_delay_reason",
            "btl_supauth_od",
            "btl_other_supauth",
            "btl_remarks",
            "btl_dpo_comment",
        ]
        labels = {
            "btl_start": _("When did the breach start?"),
            "btl_start_known": _("Is the starting time of the breach known?"),
            "btl_end": _("When did the breach end?"),
            "btl_ongoing": _("Is the breach still ongoing?"),
            "btl_may_recur": _("Is there likely to be a repeat of the breach?"),
            "btl_noticed": _("When did you become aware of the breach?"),
            "btl_notif_delay_reason": _("Reason for delay of notication (if any):"),
            "btl_supauth_od": _(
                "Supervisory authority organisational descriptor (if any and already known):"
            ),
            "btl_other_supauth": _(
                "Notification to another supervisory authority (if any):"
            ),
            "btl_remarks": _("Breach timeline remarks (optional):"),
            "btl_dpo_comment": settings.DPO_COMMENT,
        }
        help_texts = {
            "btl_dpo_comment": settings.DPO_COMMENT_HELPTEXT,
        }
        widgets = {
            "btl_start": NumberInput(attrs={"type": "date"}),
            "btl_start_known": RadioSelect(),
            "btl_end": NumberInput(attrs={"type": "date"}),
            "btl_ongoing": RadioSelect(),
            "btl_may_recur": RadioSelect(),
            "btl_noticed": NumberInput(attrs={"type": "date"}),
            "btl_notif_delay_reason": Textarea(attrs={"cols": 80, "rows": 10}),
            "btl_other_supauth": Textarea(attrs={"cols": 80, "rows": 5}),
            "btl_remarks": Textarea(attrs={"cols": 80, "rows": 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "edit-btl"
        self.helper.layout = Layout(
            Row(
                Column(
                    "btl_start_known",
                    "btl_start",
                    "btl_ongoing",
                    "btl_end",
                    "btl_may_recur",
                    "btl_noticed",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "btl_notif_delay_reason",
                    "btl_supauth_od",
                    "btl_other_supauth",
                    "btl_remarks",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Column(
                    Field(
                        "btl_dpo_comment",
                        template="dpo-comment-field.html",
                    ),
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            HTML("<p></p>"),
            Row(
                Submit("submit", _("Submit"), css_class="btn btn-primary"),
            ),
        )

    def clean(self):
        super().clean()
        err_0 = _(
            'Either select "No" for an unknown starting time or select "Yes" and enter the date the breach started.'
        )
        err_1 = _(
            'Either select "Yes" for an ongoing breach or select "No" and enter the date the breach ended.'
        )
        err_2 = _("The breach may not have ended before it started.")
        err_3 = _("Please select whether the breach is likely to happen again.")
        err_4 = _("Please enter the date you became aware of the breach.")
        if self.cleaned_data:
            if (
                not self.cleaned_data.get("btl_start")
                and self.cleaned_data.get("btl_start_known") != "no"
            ):
                self.add_error("btl_start", err_0)
                self.add_error("btl_start_known", err_0)
            if (
                not self.cleaned_data.get("btl_end")
                and self.cleaned_data.get("btl_ongoing") != "yes"
            ):
                self.add_error("btl_end", err_1)
                self.add_error("btl_ongoing", err_1)
            if self.cleaned_data.get("btl_start") and self.cleaned_data.get("btl_end"):
                delta_start = self.cleaned_data.get(
                    "btl_start"
                ) - self.cleaned_data.get("btl_end")
                if delta_start.days > 0:
                    self.add_error("btl_start", err_2)
                    self.add_error("btl_end", err_2)
            if self.cleaned_data.get("btl_may_recur") is None:
                self.add_error("btl_may_recur", err_3)
            if self.cleaned_data.get("btl_noticed") is None:
                self.add_error("btl_noticed", err_4)


class BreachDescriptionForm(ModelForm):
    class Meta:
        model = BreachDescription
        fields = [
            "bdesc_selection",
            "bdesc_selection_other",
            "bdesc_description",
            "bdesc_dpo_comment",
        ]
        labels = {
            "bdesc_selection": _(
                "Select one or more incidents, that led to the breach:"
            ),
            "bdesc_selection_other": _(
                "Enter one or more additional or other incidents, that led to the breach (one per line, if any):"
            ),
            "bdesc_description": _(
                "Actual description of the breach in your own words:"
            ),
            "bdesc_dpo_comment": settings.DPO_COMMENT,
        }
        help_texts = {
            "bdesc_dpo_comment": settings.DPO_COMMENT_HELPTEXT,
        }
        widgets = {
            "bdesc_selection_other": Textarea(attrs={"cols": 80, "rows": 10}),
            "bdesc_description": Textarea(attrs={"cols": 80, "rows": 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "edit-bdesc"
        self.helper.layout = Layout(
            Row(
                Column(
                    "bdesc_selection",
                    "bdesc_selection_other",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "bdesc_description",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Column(
                    Field(
                        "bdesc_dpo_comment",
                        template="dpo-comment-field.html",
                    ),
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            HTML("<p></p>"),
            Row(
                Submit("submit", _("Submit"), css_class="btn btn-primary"),
            ),
        )

    def clean(self):
        super().clean()
        err_0 = _("Choose or enter at least one type of breach.")
        err_1 = _("A description of the breach is required.")
        if self.cleaned_data:
            if not self.cleaned_data.get(
                "bdesc_selection"
            ) and not self.cleaned_data.get("bdesc_selection_other"):
                self.add_error("bdesc_selection", err_0)
                self.add_error("bdesc_selection_other", err_0)
            if not self.cleaned_data.get("bdesc_description"):
                self.add_error("bdesc_description", err_1)


class BreachAffectedDataForm(ModelForm):
    class Meta:
        model = BreachAffectedData
        fields = [
            "baffd_selection",
            "baffd_selection_other",
            "baffd_special_selection",
            "baffd_special_unknown_reason",
            "baffd_data_min",
            "baffd_data_max",
            "baffd_remarks",
            "baffd_dpo_comment",
        ]
        labels = {
            "baffd_selection": _(
                "Select one or more categories of data affected by the breach:"
            ),
            "baffd_selection_other": _(
                "Enter additional or other categories of data affected by the breach (one per line, if any):"
            ),
            "baffd_special_selection": _(
                "Select one or more special categories of data affected by the breach (if any):"
            ),
            "baffd_special_unknown_reason": _(
                "Reason for special categories of data being not known, yet:"
            ),
            "baffd_data_min": _(
                "Minimum estimated number of data sets affected by the breach:"
            ),
            "baffd_data_max": _(
                "Maximum estimated number of data sets affected by the breach:"
            ),
            "baffd_remarks": _("Breach affected data remarks (optional):"),
            "baffd_dpo_comment": settings.DPO_COMMENT,
        }
        help_texts = {
            "baffd_dpo_comment": settings.DPO_COMMENT_HELPTEXT,
        }
        widgets = {
            "baffd_selection_other": Textarea(attrs={"cols": 80, "rows": 10}),
            "baffd_special_unknown_reason": Textarea(attrs={"cols": 80, "rows": 10}),
            "baffd_remarks": Textarea(attrs={"cols": 80, "rows": 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "edit-baffd"
        self.helper.layout = Layout(
            Row(
                Column(
                    "baffd_selection",
                    "baffd_selection_other",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "baffd_special_selection",
                    "baffd_special_unknown_reason",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Column(
                    "baffd_data_min",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "baffd_data_max",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Column(
                    "baffd_remarks",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Column(
                    Field(
                        "baffd_dpo_comment",
                        template="dpo-comment-field.html",
                    ),
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            HTML("<p></p>"),
            Row(
                Submit("submit", _("Submit"), css_class="btn btn-primary"),
            ),
        )

    def clean(self):
        super().clean()
        err_0 = _("At least one data category is required.")
        err_1 = _("Please enter a reason for special categories of data being unknown.")
        err_2 = _("An estimated minimum number of data sets is required.")
        err_3 = _("An estimated maximum number of data sets is required.")
        if self.cleaned_data:
            if not self.cleaned_data.get(
                "baffd_selection"
            ) and not self.cleaned_data.get("baffd_selection_other"):
                self.add_error("baffd_selection", err_0)
                self.add_error("baffd_selection_other", err_0)
            if self.cleaned_data.get("baffd_special_selection"):
                if "special_not_known_yet" in self.cleaned_data.get(
                    "baffd_special_selection"
                ) and not self.cleaned_data.get("baffd_special_unknown_reason"):
                    self.add_error("baffd_special_unknown_reason", err_1)
            if not self.cleaned_data.get("baffd_data_min"):
                self.add_error("baffd_data_min", err_2)
            if not self.cleaned_data.get("baffd_data_max"):
                self.add_error("baffd_data_max", err_3)


class BreachAffectedSubjectsForm(ModelForm):
    class Meta:
        model = BreachAffectedSubjects
        fields = [
            "baffs_selection",
            "baffs_selection_other",
            "baffs_datasubjects_min",
            "baffs_datasubjects_max",
            "baffs_remarks",
            "baffs_dpo_comment",
        ]
        labels = {
            "baffs_selection": _(
                "Select one or more categories of data subjects affected by the breach:"
            ),
            "baffs_selection_other": _(
                "Enter additional or other categories of data subjects affected by the breach (one per line, if any):"
            ),
            "baffs_datasubjects_min": _(
                "Minimum estimated number of data subjects affected by the breach:"
            ),
            "baffs_datasubjects_max": _(
                "Maximum estimated number of data subjects affected by the breach:"
            ),
            "baffs_remarks": _("Breach affected data subjects remarks (optional):"),
            "baffs_dpo_comment": settings.DPO_COMMENT,
        }
        help_texts = {
            "baffs_dpo_comment": settings.DPO_COMMENT_HELPTEXT,
        }
        widgets = {
            "baffs_selection_other": Textarea(attrs={"cols": 80, "rows": 5}),
            "baffs_remarks": Textarea(attrs={"cols": 80, "rows": 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "edit-baffs"
        self.helper.layout = Layout(
            Row(
                Column(
                    "baffs_selection",
                    "baffs_selection_other",
                    "baffs_datasubjects_min",
                    "baffs_datasubjects_max",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "baffs_remarks",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Column(
                    Field(
                        "baffs_dpo_comment",
                        template="dpo-comment-field.html",
                    ),
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            HTML("<p></p>"),
            Row(
                Submit("submit", _("Submit"), css_class="btn btn-primary"),
            ),
        )

    def clean(self):
        super().clean()
        err_0 = _("At least one data subject category is required.")
        err_1 = _("An estimated minimum number of data subjects is required.")
        err_2 = _("An estimated maximum number of data subjects is required.")
        if self.cleaned_data:
            if not self.cleaned_data.get(
                "baffs_selection"
            ) and not self.cleaned_data.get("baffs_selection_other"):
                self.add_error("baffs_selection", err_0)
                self.add_error("baffs_selection_other", err_0)
            if not self.cleaned_data.get("baffs_datasubjects_min"):
                self.add_error("baffs_datasubjects_min", err_1)
            if not self.cleaned_data.get("baffs_datasubjects_max"):
                self.add_error("baffs_datasubjects_max", err_2)


class BreachConsequencesForm(ModelForm):
    class Meta:
        model = BreachConsequences
        fields = [
            "bcons_confidentiality_selection",
            "bcons_confidentiality",
            "bcons_integrity_selection",
            "bcons_integrity",
            "bcons_availability_selection",
            "bcons_availability",
            "bcons_consequences_descr",
            "bcons_dpo_comment",
        ]
        labels = {
            "bcons_confidentiality_selection": _(
                "Selection of consequences for confidentiality:"
            ),
            "bcons_confidentiality": _(
                "Additional or other consequences for confidentiality (one per line, if any):"
            ),
            "bcons_integrity_selection": _("Selection of consequences for integrity:"),
            "bcons_integrity": _(
                "Additional or other consequences for integrity (one per line, if any):"
            ),
            "bcons_availability_selection": _(
                "Selection of consequences for availability:"
            ),
            "bcons_availability": _(
                "Additional or other consequences for availability (one per line, if any):"
            ),
            "bcons_consequences_descr": _(
                "Description of likely consequences of the breach:"
            ),
            "bcons_dpo_comment": settings.DPO_COMMENT,
        }
        help_texts = {
            "bcons_dpo_comment": settings.DPO_COMMENT_HELPTEXT,
        }
        widgets = {
            "bcons_confidentiality": Textarea(attrs={"cols": 80, "rows": 5}),
            "bcons_integrity": Textarea(attrs={"cols": 80, "rows": 5}),
            "bcons_availability": Textarea(attrs={"cols": 80, "rows": 5}),
            "bcons_consequences_descr": Textarea(attrs={"cols": 80, "rows": 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "edit-bcons"
        self.helper.layout = Layout(
            Row(
                Column(
                    "bcons_confidentiality_selection",
                    "bcons_confidentiality",
                    "bcons_integrity_selection",
                    "bcons_integrity",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "bcons_availability_selection",
                    "bcons_availability",
                    "bcons_consequences_descr",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Column(
                    Field(
                        "bcons_dpo_comment",
                        template="dpo-comment-field.html",
                    ),
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            HTML("<p></p>"),
            Row(
                Submit("submit", _("Submit"), css_class="btn btn-primary"),
            ),
        )

    def clean(self):
        super().clean()
        err_0 = _("At least one likely consequence is required.")
        err_1 = _("A description of likely consequences is required.")
        if self.cleaned_data:
            if (
                not self.cleaned_data.get("bcons_confidentiality_selection")
                and not self.cleaned_data.get("bcons_confidentiality")
                and not self.cleaned_data.get("bcons_integrity_selection")
                and not self.cleaned_data.get("bcons_integrity")
                and not self.cleaned_data.get("bcons_availability_selection")
                and not self.cleaned_data.get("bcons_availability")
            ):
                self.add_error("bcons_confidentiality_selection", err_0)
                self.add_error("bcons_confidentiality", err_0)
                self.add_error("bcons_integrity_selection", err_0)
                self.add_error("bcons_integrity", err_0)
                self.add_error("bcons_availability_selection", err_0)
                self.add_error("bcons_availability", err_0)
            if not self.cleaned_data.get("bcons_consequences_descr"):
                self.add_error("bcons_consequences_descr", err_1)


class BreachMeasuresForm(ModelForm):
    class Meta:
        model = BreachMeasures
        fields = [
            "bmeasures_taken",
            "bmeasures_proposed",
            "bmeasures_no_measures_reason",
            "bmeasures_dpo_comment",
        ]
        labels = {
            "bmeasures_taken": _(
                "Description of measures taken concerning the breach:"
            ),
            "bmeasures_proposed": _(
                "Description of measures proposed concerning the breach:"
            ),
            "bmeasures_no_measures_reason": _(
                "Reason for no measures taken or proposed, if any:"
            ),
            "bmeasures_dpo_comment": settings.DPO_COMMENT,
        }
        help_texts = {
            "bmeasures_dpo_comment": settings.DPO_COMMENT_HELPTEXT,
        }
        widgets = {
            "bmeasures_taken": Textarea(attrs={"cols": 80, "rows": 10}),
            "bmeasures_proposed": Textarea(attrs={"cols": 80, "rows": 10}),
            "bmeasures_no_measures_reason": Textarea(attrs={"cols": 80, "rows": 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "edit-bmeasures"
        self.helper.layout = Layout(
            Row(
                Column(
                    "bmeasures_taken",
                    "bmeasures_proposed",
                    "bmeasures_no_measures_reason",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Column(
                    Field(
                        "bmeasures_dpo_comment",
                        template="dpo-comment-field.html",
                    ),
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            HTML("<p></p>"),
            Row(
                Submit("submit", _("Submit"), css_class="btn btn-primary"),
            ),
        )

    def clean(self):
        super().clean()
        err_0 = _("There must be a reason for no measures taken or proposed.")
        if self.cleaned_data:
            if not self.cleaned_data.get("bmeasures_no_measures_reason"):
                if not self.cleaned_data.get(
                    "bmeasures_taken"
                ) and not self.cleaned_data.get("bmeasures_proposed"):
                    self.add_error("bmeasures_no_measures_reason", err_0)


class BreachCommunicationForm(ModelForm):
    class Meta:
        model = BreachCommunication
        fields = [
            "bcomm_communication_selection",
            "bcomm_no_communication_reason",
            "bcomm_modality_selection",
            "bcomm_modality",
            "bcomm_number_of_data_subjects",
            "bcomm_remarks",
            "bcomm_dpo_comment",
        ]
        labels = {
            "bcomm_communication_selection": _("Communication selection:"),
            "bcomm_no_communication_reason": _(
                "Reason for not communicating the breach:"
            ),
            "bcomm_modality_selection": _("Modalities of communication selection:"),
            "bcomm_modality": _(
                "Additional or other modalities of communication (one per line, if any):"
            ),
            "bcomm_number_of_data_subjects": _(
                "Number of persons already informed and/or to be informed:"
            ),
            "bcomm_remarks": _(
                "Remarks regarding breach communication to the data subjects (if any):"
            ),
            "bcomm_dpo_comment": settings.DPO_COMMENT,
        }
        help_texts = {
            "bcomm_dpo_comment": settings.DPO_COMMENT_HELPTEXT,
        }
        widgets = {
            "bcomm_communication_selection": RadioSelect(),
            "bcomm_no_communication_reason": Textarea(attrs={"cols": 80, "rows": 10}),
            "bcomm_modality": Textarea(attrs={"cols": 80, "rows": 5}),
            "bcomm_remarks": Textarea(attrs={"cols": 80, "rows": 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "edit-bcomm"
        self.helper.layout = Layout(
            Row(
                Column(
                    "bcomm_communication_selection",
                    "bcomm_remarks",
                    "bcomm_no_communication_reason",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "bcomm_modality_selection",
                    "bcomm_modality",
                    "bcomm_number_of_data_subjects",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Column(
                    Field(
                        "bcomm_dpo_comment",
                        template="dpo-comment-field.html",
                    ),
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            HTML("<p></p>"),
            Row(
                Submit("submit", _("Submit"), css_class="btn btn-primary"),
            ),
        )

    def clean(self):
        super().clean()
        err_0 = _("Please select a communication choice.")
        err_1 = _("Please enter a reason for no communication intended.")
        err_2 = _(
            "Please make remarks concerning communication done, underway or considered."
        )
        if self.cleaned_data:
            if not self.cleaned_data.get("bcomm_communication_selection"):
                self.add_error("bcomm_communication_selection", err_0)
            if self.cleaned_data.get("bcomm_communication_selection"):
                if "will_not_happen" in self.cleaned_data.get(
                    "bcomm_communication_selection"
                ) and not self.cleaned_data.get("bcomm_no_communication_reason"):
                    self.add_error("bcomm_no_communication_reason", err_1)
            if self.cleaned_data.get("bcomm_communication_selection"):
                if not self.cleaned_data.get(
                    "bcomm_remarks"
                ) and "already_happened" in self.cleaned_data.get(
                    "bcomm_communication_selection"
                ):
                    self.add_error("bcomm_remarks", err_2)
            if self.cleaned_data.get("bcomm_communication_selection"):
                if not self.cleaned_data.get(
                    "bcomm_remarks"
                ) and "not_happened_yet" in self.cleaned_data.get(
                    "bcomm_communication_selection"
                ):
                    self.add_error("bcomm_remarks", err_2)
            if self.cleaned_data.get("bcomm_communication_selection"):
                if not self.cleaned_data.get(
                    "bcomm_remarks"
                ) and "may_happen" in self.cleaned_data.get(
                    "bcomm_communication_selection"
                ):
                    self.add_error("bcomm_remarks", err_2)

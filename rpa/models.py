""" RPA generator models.py
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from multiselectfield import MultiSelectField


class Rpa(models.Model):
    """RPA main class; contains RPA slug (short name), rpa_bumper
    (serves for confirmation purposes) and helptext_display_default
    (help text collapsible box state preset)
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rpas", null=True
    )
    slug = models.SlugField(
        unique=True,
        max_length=20,
    )
    rpa_bumper = models.BooleanField()
    helptext_display_default = models.CharField(
        max_length=20, blank=True, default="show"
    )

    class Meta:
        verbose_name = _("RPA slug")
        verbose_name_plural = _("RPA slugs")

    def __str__(self):
        return str(self.slug)


class ProcessingActivityName(models.Model):
    """Holds RPA designation and meta data (descriptive long name, date
    of introduction, etc.)
    """

    rpa = models.ForeignKey(Rpa, on_delete=models.CASCADE, related_name="rpa_names")
    name = models.CharField(max_length=200, blank=True)
    is_new = models.BooleanField(blank=True, null=True)
    date_intro = models.DateField(blank=True, null=True)
    has_changed = models.BooleanField(blank=True, null=True)
    date_changed = models.DateField(blank=True, null=True)
    former_name = models.CharField(max_length=200, blank=True)
    cname = "RPA designation"

    class Meta:
        verbose_name = _("Record of processing activities")
        verbose_name_plural = _("Records of processing activities")

    def __str__(self):
        return f"{self.rpa.slug} {self.cname}"


class DataController(models.Model):
    """Holds data controller contact information"""

    rpa = models.ForeignKey(
        Rpa, on_delete=models.CASCADE, related_name="datacontrollers"
    )
    dcon_name = models.CharField(
        max_length=100,
        default=settings.CONTROLLER_NAME,
    )
    dcon_repby = models.CharField(
        max_length=100,
        default=settings.CONTROLLER_REPBY,
        blank=True,
    )
    dcon_street = models.CharField(
        max_length=100,
        default=settings.CONTROLLER_STREET,
    )
    dcon_pcode = models.CharField(
        max_length=10,
        default=settings.CONTROLLER_PCODE,
    )
    dcon_city = models.CharField(
        max_length=50,
        default=settings.CONTROLLER_CITY,
    )
    dcon_country = models.CharField(
        max_length=50,
        default=settings.CONTROLLER_COUNTRY,
    )
    dcon_phone = models.CharField(
        max_length=30,
        default=settings.CONTROLLER_PHONE,
    )
    dcon_email = models.EmailField(
        default=settings.CONTROLLER_EMAIL,
    )
    dcon_web = models.URLField(
        default=settings.CONTROLLER_WEB,
        blank=True,
    )
    cname = "data controller"

    class Meta:
        verbose_name = _("Data controller")
        verbose_name_plural = _("Data controllers")

    def __str__(self):
        return f"{self.rpa.slug} {self.cname}"


class JointController(models.Model):
    """Holds joint controller contact information"""

    rpa = models.ForeignKey(
        Rpa, on_delete=models.CASCADE, related_name="jointcontrollers"
    )
    jcon_exists = models.BooleanField(
        blank=True,
        null=True,
    )
    jcon_name = models.CharField(
        max_length=100,
        blank=True,
    )
    jcon_repby = models.CharField(
        max_length=100,
        blank=True,
    )
    jcon_street = models.CharField(
        max_length=100,
        blank=True,
    )
    jcon_pcode = models.CharField(
        max_length=10,
        blank=True,
    )
    jcon_city = models.CharField(
        max_length=50,
        blank=True,
    )
    jcon_country = models.CharField(
        max_length=50,
        blank=True,
    )
    jcon_contact = models.TextField(
        max_length=500,
        blank=True,
    )
    cname = "joint controller"

    class Meta:
        verbose_name = _("Joint controller")
        verbose_name_plural = _("Joint controllers")

    def __str__(self):
        return f"{self.rpa.slug} {self.cname}"


class DataProtectionOfficer(models.Model):
    """Holds data protection officer contact information"""

    rpa = models.ForeignKey(Rpa, on_delete=models.CASCADE, related_name="dpos")
    dpo_name = models.CharField(
        max_length=100,
        default=settings.DPO_NAME,
    )
    dpo_street = models.CharField(
        max_length=100,
        default=settings.DPO_STREET,
    )
    dpo_pcode = models.CharField(
        max_length=10,
        default=settings.DPO_PCODE,
    )
    dpo_city = models.CharField(
        max_length=50,
        default=settings.DPO_CITY,
    )
    dpo_country = models.CharField(
        max_length=50,
        default=settings.DPO_COUNTRY,
    )
    dpo_phone = models.CharField(
        max_length=30,
        default=settings.DPO_PHONE,
    )
    dpo_email = models.EmailField(
        default=settings.DPO_EMAIL,
    )
    dpo_web = models.URLField(
        blank=True,
        default=settings.DPO_WEB,
    )
    cname = "dpo"

    class Meta:
        verbose_name = _("Data protection officer")
        verbose_name_plural = _("Data protection officers")

    def __str__(self):
        return f"{self.rpa.slug} {self.cname}"


class InternallyResponsibleDept(models.Model):
    """Holds contact information of the internally responsible
    department; this is not explicitly mentioned in the GDPR, but in a
    large entity, you want to know who is actually doing things
    """

    rpa = models.ForeignKey(
        Rpa, on_delete=models.CASCADE, related_name="internally_resp_depts"
    )
    ird_name = models.CharField(
        max_length=100,
        blank=True,
    )
    ird_street = models.CharField(
        max_length=100,
        blank=True,
    )
    ird_pcode = models.CharField(
        max_length=10,
        blank=True,
    )
    ird_city = models.CharField(
        max_length=50,
        blank=True,
    )
    ird_country = models.CharField(
        max_length=50,
        blank=True,
    )
    ird_phone = models.CharField(
        max_length=30,
        blank=True,
    )
    ird_email = models.EmailField()
    ird_comments = models.TextField(
        max_length=500,
        blank=True,
    )
    cname = "internally resp."

    class Meta:
        verbose_name = _("Internally responsible department")
        verbose_name_plural = _("Internally responsible departments")

    def __str__(self):
        return f"{self.rpa.slug} {self.cname}"


class CategoryOfPersonalData(models.Model):
    """Holds a single category of personal data to be processed"""

    rpa = models.ForeignKey(
        Rpa, on_delete=models.CASCADE, related_name="datacategories"
    )
    cpd_index = models.PositiveSmallIntegerField(
        blank=True, null=True, choices=list(zip(range(1, 10), range(1, 10)))
    )
    cpd_name = models.CharField(max_length=80, blank=True)
    cpd_is_special = models.BooleanField(default=False)
    cname = "data categories"

    class Meta:
        verbose_name = _("Category of personal data")
        verbose_name_plural = _("Categories of personal data")
        ordering = ["cpd_index"]

    def __str__(self):
        return f"{self.rpa.slug} {self.cname}"


class CategoriesOfPersonalDataOrigin(models.Model):
    """Holds a textual description of the origin of the categories of personal data to be processed"""

    rpa = models.ForeignKey(
        Rpa, on_delete=models.CASCADE, related_name="datacategories_origin"
    )
    cpdo_descr = models.TextField(max_length=1000, blank=True)
    cname = "data categories origin"

    class Meta:
        verbose_name = _("Categories of personal data origin")
        verbose_name_plural = _("Categories of personal data origins")

    def __str__(self):
        return f"{self.rpa.slug} {self.cname}"


class PurposeAndLegalBasis(models.Model):
    """Holds purpose and legal basis of the processing activity"""

    PLB_CHOICES = (
        (
            "plb_art6_1a",
            _("Art. 6(1)(a) GDPR (consent of the data subject)"),
        ),
        (
            "plb_art6_1b",
            _(
                "Art. 6(1)(b) GDPR (performance of a contract to which the data subject is party)"
            ),
        ),
        (
            "plb_art6_1c",
            _("Art. 6(1)(c) GDPR (legal obligations of the data controller)"),
        ),
        (
            "plb_art6_1d",
            _(
                "Art. 6(1)(d) GDPR (protection of the vital interests of the data subject or of another natural person)"
            ),
        ),
        (
            "plb_art6_1e",
            _(
                "Art. 6(1)(e) GDPR (performance of a task carried out in the public interest or in the exercise of official authority vested in the controller)"
            ),
        ),
        (
            "plb_art6_1f",
            _(
                "Art. 6(1)(f) GDPR (purposes of the legitimate interests pursued by the controller - not applicable for public authorities!)"
            ),
        ),
        ("plb_art9_2", _("Art. 9(2) GDPR (as described in the reasons)")),
        (
            "plb_art88_1",
            _(
                "Art. 88(1) GDPR plus local legislation (processing of data concerning employees or job applicants for administrative purposes)"
            ),
        ),
    )
    rpa = models.ForeignKey(
        Rpa, on_delete=models.CASCADE, related_name="purposes_legalbases"
    )
    plb_purpose = models.TextField(
        max_length=1000,
    )
    plb = MultiSelectField(choices=PLB_CHOICES, max_length=250, default="")
    plb_reasons = models.TextField(
        max_length=1000,
    )
    cname = "purpose/legal basis"

    class Meta:
        verbose_name = _("Purpose and legal basis")
        verbose_name_plural = _("Purposes and legal bases")

    def __str__(self):
        return f"{self.rpa.slug} {self.cname}"


class DataSubject(models.Model):
    """Holds a single data subject category; dsub_cpd_sel is meant
    to hold a list of data categories processed concerning the data
    subject
    """

    rpa = models.ForeignKey(Rpa, on_delete=models.CASCADE, related_name="datasubjects")
    cpd = models.ManyToManyField(CategoryOfPersonalData, related_name="datasubjects")
    dsub_name = models.CharField(max_length=80)
    dsub_cpd_sel = models.CharField(max_length=500, blank=True)
    cname = "data subjects"

    class Meta:
        verbose_name = _("Data subject")
        verbose_name_plural = _("Data subjects")

    def __str__(self):
        return f"{self.rpa.slug} {self.cname}"


class TimeLimitForErasure(models.Model):
    """Holds a single time limit for erasure; tle_cpd_sel is meant to
    hold a list of data categories processed for which the time limit
    applies
    """

    TLE_HANDLING_CHOICES = [
        (
            "tle_in_annex",
            _("A data erasure concept exists and is attached to the annex."),
        ),
        ("tle_in_rpa", _("Time limits for erasure are described below.")),
    ]

    rpa = models.ForeignKey(
        Rpa, on_delete=models.CASCADE, related_name="timelimits_erasure"
    )
    cpd = models.ManyToManyField(CategoryOfPersonalData, related_name="timelimits")
    tle_handling = models.CharField(
        max_length=50, default="", blank=True, null=True, choices=TLE_HANDLING_CHOICES
    )
    tle_start = models.CharField(max_length=200, blank=True)
    tle_length = models.CharField(max_length=200, blank=True)
    tle_cpd_sel = models.CharField(max_length=500, blank=True)
    tle_comment = models.TextField(
        max_length=1000,
        blank=True,
    )
    cname = "erasure limits"

    class Meta:
        verbose_name = _("Time limit for erasure")
        verbose_name_plural = _("Time limits for erasure")

    def __str__(self):
        return f"{self.rpa.slug} {self.cname}"


class CategoryOfRecipients(models.Model):
    """Holds a single internal or external category of recipients;
    crec_cpd_sel is meant to hold a list of data categories to be
    transferred to the respective category of recipients
    """

    CREC_HANDLING_CHOICES = [
        ("crec_no_crec", _("No: There are no categories of recipients.")),
        (
            "crec_in_annex",
            _(
                "Yes: Categories of recipients are described in a separate document that is attached to the annex."
            ),
        ),
        ("crec_in_rpa", _("Yes: Categories of recipients are described below.")),
    ]

    rpa = models.ForeignKey(
        Rpa, on_delete=models.CASCADE, related_name="categories_of_rec"
    )
    cpd = models.ManyToManyField(CategoryOfPersonalData, related_name="recipients")
    crec_handling = models.CharField(
        max_length=50, default="", blank=True, null=True, choices=CREC_HANDLING_CHOICES
    )
    crec_designation = models.TextField(
        max_length=500,
        blank=True,
    )
    crec_is_external = models.BooleanField(blank=True, null=True)
    crec_cpd_sel = models.CharField(max_length=500, blank=True)
    cname = "Cat. of recipients"

    class Meta:
        verbose_name = _("Category of recipients")
        verbose_name_plural = _("Categories of recipients")

    def __str__(self):
        return f"{self.rpa.slug} {self.cname}"


class TransferToThirdCountry(models.Model):
    """Holds information about data transfers to a third country or
    international organisation; this usually requires free text
    explanations (ttc_3rdcountry, ttc_non_adequacy_explanation)
    """

    TTC_NON_ADEQUACY_CHOICES = (
        (
            "ttc_lbaei",
            _("Art. 46(2)(a) GDPR (legally binding and enforceable instrument)"),
        ),
        ("ttc_bcr", _("Art. 46(2)(b) GDPR (binding corporate rules)")),
        ("ttc_sdpc", _("Art. 46(2)(c) GDPR (standard DP clauses)")),
        ("ttc_coc", _("Art. 46(2)(e) GDPR (approved code of conduct)")),
        ("ttc_cert", _("Art. 46(2)(f) GDPR (certification)")),
        ("ttc_except", _("Art. 49 GDPR (derogations for specific situations)")),
    )
    rpa = models.ForeignKey(
        Rpa, on_delete=models.CASCADE, related_name="transfers_to_3rdc"
    )
    ttc_3rdcountry_intended = models.BooleanField(blank=True, null=True)
    ttc_3rdcountry = models.TextField(
        max_length=500,
        blank=True,
    )
    ttc_3rdcountry_adequacy = models.BooleanField(blank=True, null=True)
    ttc_non_adequacy_choices = MultiSelectField(
        choices=TTC_NON_ADEQUACY_CHOICES, max_length=250, default="", blank=True
    )
    ttc_non_adequacy_explanation = models.TextField(
        max_length=1000,
        blank=True,
    )
    cname = "transfer to 3rd c."

    class Meta:
        verbose_name = _("Transfer to third countries")
        verbose_name_plural = _("Transfers to third countries")

    def __str__(self):
        return f"{self.rpa.slug} {self.cname}"


class AccessGroup(models.Model):
    """Holds information about groups that have access to personal data
    categories; agrp_cpd_sel holds a list of the data categories by
    access group - access group is not a GDPR term, but the requirement
    to describe access groups can be derived from Art. 5(1)(f) GDPR,
    Art. 32(4) GDPR
    """

    AGRP_HANDLING_CHOICES = [
        (
            "agrp_in_annex",
            _("There is an authorization/role concept that is attached to the annex."),
        ),
        ("agrp_in_rpa", _("Access groups are described below.")),
    ]

    rpa = models.ForeignKey(Rpa, on_delete=models.CASCADE, related_name="accessgroups")
    cpd = models.ManyToManyField(CategoryOfPersonalData, related_name="accessgroups")
    agrp_handling = models.CharField(
        max_length=50, default="", blank=True, null=True, choices=AGRP_HANDLING_CHOICES
    )
    agrp_name = models.CharField(
        max_length=120,
        blank=True,
        default="",
    )
    agrp_can_read = models.BooleanField(
        blank=True,
        null=True,
    )
    agrp_can_edit = models.BooleanField(
        blank=True,
        null=True,
    )
    agrp_can_delete = models.BooleanField(
        blank=True,
        null=True,
    )
    agrp_cpd_sel = models.CharField(max_length=500, blank=True)
    cname = "access groups"

    class Meta:
        verbose_name = _("Access group")
        verbose_name_plural = _("Access groups")

    def __str__(self):
        return f"{self.rpa.slug} {self.cname}"


class Transparency(models.Model):
    """Holds transparency information (the way data subjects will be informed
    about the processing of their data)
    """

    TRAN_CHOICES = (
        (
            "tran_leaflet",
            _(
                "Data subjects will be informed via a leaflet (attached and listed in annex)"
            ),
        ),
        (
            "tran_online",
            _("Data subjects will be informed online (cf. link in explanation)"),
        ),
        (
            "tran_other",
            _(
                "Data subjects will be informed in another way (as described in explanation)"
            ),
        ),
    )
    rpa = models.ForeignKey(
        Rpa, on_delete=models.CASCADE, related_name="transparencies"
    )
    tran_choices = MultiSelectField(
        choices=TRAN_CHOICES, max_length=250, default="", blank=True
    )
    tran_explanation = models.TextField(
        max_length=1000,
        blank=True,
    )
    cname = "transparency"

    class Meta:
        verbose_name = _("Transparency")
        verbose_name_plural = _("Transparencies")

    def __str__(self):
        return f"{self.rpa.slug} {self.cname}"


class DataProcessor(models.Model):
    """Holds data processor contact information"""

    rpa = models.ForeignKey(
        Rpa, on_delete=models.CASCADE, related_name="dataprocessors"
    )
    dpro_is_assigned = models.BooleanField(
        blank=True,
        null=True,
    )
    dpro_dpa_in_annex = models.BooleanField(
        blank=True,
        null=True,
    )
    dpro_name = models.CharField(
        max_length=100,
        blank=True,
    )
    dpro_street = models.CharField(
        max_length=100,
        blank=True,
    )
    dpro_pcode = models.CharField(
        max_length=10,
        blank=True,
    )
    dpro_city = models.CharField(
        max_length=50,
        blank=True,
    )
    dpro_country = models.CharField(
        max_length=50,
        blank=True,
    )
    dpro_contact = models.TextField(
        max_length=500,
        blank=True,
    )
    cname = "data processor"

    class Meta:
        verbose_name = _("Data processor")
        verbose_name_plural = _("Data processors")

    def __str__(self):
        return f"{self.rpa.slug} {self.cname}"


class PrivacyImpactAssessment(models.Model):
    """Holds privacy impact assessment (correct term: data protection
    impact assessment) information
    """

    PIA_NR_CHOICES = (
        (
            "pia_nr_automated_processing",
            _(
                "There is no systematic and extensive evaluation of personal aspects relating to natural persons which is based on automated processing."
            ),
        ),
        (
            "pia_nr_special_categories",
            _(
                "There is no processing on a large scale of special categories of data referred to in GDPR Article 9."
            ),
        ),
        (
            "pia_nr_monitoring_public",
            _(
                "There is no systematic monitoring of a publicly accessible area on a large scale."
            ),
        ),
        (
            "pia_nr_required_list",
            _(
                'The processing operation is not on the "required-list" issued by the competent supervisory authority.'
            ),
        ),
    )
    PIA_RESULTS = (
        (
            "pia_sufficient_measures",
            _(
                "Measures taken are sufficient (as described in the attached document listed in the annex)."
            ),
        ),
        (
            "pia_additional_measures",
            _(
                "Additional measures were taken (as described in the attached document listed in the annex)."
            ),
        ),
        (
            "pia_supauth_consulted",
            _(
                "No additional measures could be taken and therefore the supervisory authority had to be consulted (result is attached and listed in the annex)."
            ),
        ),
    )
    rpa = models.ForeignKey(Rpa, on_delete=models.CASCADE, related_name="pias")
    pia_required = models.BooleanField(blank=True, null=True)
    pia_not_required_reason = MultiSelectField(
        choices=PIA_NR_CHOICES,
        max_length=250,
        default="",
        blank=True,
    )
    pia_results = MultiSelectField(
        choices=PIA_RESULTS, max_length=250, default="", blank=True
    )
    cname = "PIA"

    class Meta:
        verbose_name = _("Privacy impact assessment")
        verbose_name_plural = _("Privacy impact assessments")

    def __str__(self):
        return f"{self.rpa.slug} {self.cname}"


class TOM(models.Model):
    """Holds information about technical and organisational measures"""

    TOM_HANDLING_CHOICES = [
        (
            "tom_certified",
            _(
                "The processing activity has been examined and certified (corresponding documents are attached and listed in annex)"
            ),
        ),
        (
            "tom_it_security_policy",
            _(
                "The processing activity is in accordance with an existing data security concept (corresponding documents are attached and listed in annex)"
            ),
        ),
        (
            "tom_in_annex",
            _(
                "TOMs are described in a separate document (attached and listed in annex)"
            ),
        ),
        ("tom_in_rpa", _("TOMs are described below")),
    ]
    TOM_PSEUDONYMIZATION_CHOICES = [
        (
            "tom_pseudo_no_pseudo",
            _(
                "The purpose of the processing activity does not allow pseudonymisation."
            ),
        ),
        (
            "tom_pseudo_only_pseudo",
            _(
                "The processing is done with pseudonymised personal data only. Details (including the pseudonymisation method actually used) are described in the field below."
            ),
        ),
        (
            "tom_pseudo_no_repeal",
            _(
                "Pseudonymisation will never be repealed during the processing activity."
            ),
        ),
        (
            "tom_pseudo_alloc_separate",
            _(
                "Pseudonymised data and pseudonymisation allocation lists will be processed separately."
            ),
        ),
        (
            "tom_pseudo_alloc_priv",
            _(
                "Pseudonymisation allocation lists will be restricted and can be accessed by privileged personnel only (as described below)."
            ),
        ),
        (
            "tom_pseudo_alloc_enc",
            _(
                "Pseudonymisation allocation lists will be stored state-of-the-art encrypted."
            ),
        ),
    ]
    TOM_ENCRYPTION_CHOICES = [
        (
            "tom_enc_public_net",
            _(
                "State-of-the-art end-to-end encryption will always be used when personal data is transmitted via public networks (including VPN access)."
            ),
        ),
        (
            "tom_enc_store",
            _(
                "State-of-the-art encryption will always be used when data is at rest (stored)."
            ),
        ),
        (
            "tom_enc_key_unique",
            _(
                "Every allowed person accesses the data with an individual key for decryption."
            ),
        ),
        (
            "tom_enc_key_dist",
            _("Distribution of required keys to access encrypted data is documented."),
        ),
        (
            "tom_enc_key_expire",
            _(
                "There is a proven way to void existing keys (e.g. in case of a person retiring)."
            ),
        ),
    ]
    TOM_INTEGRITY_CHOICES = [
        (
            "tom_int_password",
            _(
                "Devices used for processing are password protected at all times (reduces risk of data loss)."
            ),
        ),
        (
            "tom_int_no_mobile",
            _(
                "Personal data will not be processed on mobile devices (reduces risk of data loss)."
            ),
        ),
        (
            "tom_int_no_private",
            _(
                "Personal data will not be processed on private, i.e. user owned and administered devices (reduces risk of data loss)."
            ),
        ),
        (
            "tom_int_trusted_only",
            _(
                "Personal data will only be processed on devices administered by central IT services (reduces risk of data loss)."
            ),
        ),
        (
            "tom_int_no_stud",
            _(
                "Personal data will not be processed by student assistants (reduces risk of data loss)."
            ),
        ),
        (
            "tom_int_malware",
            _(
                "Systems known to be prone to malware used for processing are regularly checked for infestation (reduces risk of data loss)."
            ),
        ),
        (
            "tom_int_secure_net",
            _(
                "The devices used for processing are all located in a separate subnet protected by a packet filter firewall administered by qualified personnel."
            ),
        ),
        (
            "tom_int_roles",
            _(
                "Systems used for processing implement role-based access (reduces risk of data loss)."
            ),
        ),
        (
            "tom_int_policy_conduct",
            _(
                "The latest version of the data protection code of conduct issued by the data controller is known to all persons processing data."
            ),
        ),
        (
            "tom_int_old_medium",
            _(
                "Decommissioned or malfunctioning storage media are forwarded to central services for destruction."
            ),
        ),
        (
            "tom_int_leak_aware",
            _(
                "All persons involved with the processing are aware that data leaks or the possibility thereof must be reported to the DPO or the supervisory authority."
            ),
        ),
    ]
    TOM_AVAILABILITY_CHOICES = [
        (
            "tom_avail_no_conseq",
            _(
                "Unavailability of the processing activity or the data (except if concomitant with a data leak) are unlikely to entail negative consequences for data subjects."
            ),
        ),
        (
            "tom_avail_backup",
            _(
                "Data is backed up in the backup system operated by central IT services."
            ),
        ),
        (
            "tom_avail_backup_self",
            _("Data is backed up in a self-operated state-of-the-art backup system."),
        ),
        (
            "tom_avail_standin",
            _("There is a stand-in arrangement for the processing activity."),
        ),
        (
            "tom_avail_documented_structure",
            _("The structure of the data (e.g. table format) is documented."),
        ),
        (
            "tom_avail_software",
            _(
                "The software used for the processing activity is actively maintained by it's vendor."
            ),
        ),
        (
            "tom_avail_plan",
            _(
                "There is a resilience plan in place that includes the processing activity."
            ),
        ),
        (
            "tom_avail_plan_check",
            _("The resilience plan is checked regularly for proper operation."),
        ),
        (
            "tom_avail_plan_hw",
            _("The resilience plan includes measures for hardware failure."),
        ),
    ]
    TOM_EVALUATION_CHOICES = [
        (
            "tom_eval_guidelines_self",
            _(
                "Relevant local guidelines, such as security concepts, resilience plans, etc. are revised on a regular basis."
            ),
        ),
        (
            "tom_eval_guidelines_known",
            _(
                "Measures are taken to ensure, that the latest versions of relevant local and central guidelines issued by the data controller are known to all persons processing data."
            ),
        ),
        (
            "tom_eval_check_weaknesses",
            _(
                "Frequent checks are carried out for known weaknesses in the systems used for the processing activity."
            ),
        ),
        (
            "tom_eval_pentesting",
            _(
                "Penetration testing is carried out on a regular basis against the systems used for the processing activity."
            ),
        ),
    ]
    TOM_APPROPRIATION_CHOICES = [
        (
            "tom_appro_not_here",
            _(
                "Measures regarding appropriation are described elsewhere (as referenced below)."
            ),
        ),
        (
            "tom_appro_awareness",
            _(
                "The purpose and the legal basis of the processing activity is known to all persons processing data."
            ),
        ),
        (
            "tom_appro_change",
            _(
                "There is a documented procedure for purpose changes that includes consultation of the DPO."
            ),
        ),
        (
            "tom_appro_onetime",
            _(
                "The processing activity is a one-time only activity, purpose changes will not be considered."
            ),
        ),
    ]
    TOM_TRANSPARENCY_CHOICES = [
        (
            "tom_tran_not_here",
            _(
                "Measures regarding transparency are described elsewhere (as referenced below)."
            ),
        ),
        (
            "tom_tran_proc",
            _(
                "There is a documented process for handling data subject enquiries that includes documentation of enquiries."
            ),
        ),
        (
            "tom_tran_db_ext",
            _(
                "The system used for the processing activity allows storage of transparency-related data, such as lock flags, fields for notes on consent, objection, etc."
            ),
        ),
        (
            "tom_tran_precompiled_ans",
            _(
                "Care is taken to ensure that precompiled and individual answers to enquiries contain all required information and are written in comprehensible language."
            ),
        ),
    ]
    TOM_SUBJECT_RIGHTS_CHOICES = [
        (
            "tom_srights_not_here",
            _(
                "Measures regarding subject rights are described elsewhere (as referenced below)."
            ),
        ),
        (
            "tom_srights_known",
            _(
                "All persons processing data have at least basic knowledge about subject rights and know how to deal with enquiries."
            ),
        ),
        (
            "tom_srights_interface",
            _(
                "The system used for the processing activity has an interface that allows easy retrieval of subject rights-related data."
            ),
        ),
    ]
    rpa = models.ForeignKey(Rpa, on_delete=models.CASCADE, related_name="toms")
    tom_handling = models.CharField(
        max_length=50, default="", blank=True, choices=TOM_HANDLING_CHOICES
    )
    tom_pseudonym_selection = MultiSelectField(
        choices=TOM_PSEUDONYMIZATION_CHOICES, max_length=1000, default="", blank=True
    )
    tom_pseudonym = models.TextField(
        blank=True,
        max_length=2000,
    )
    tom_encryption_selection = MultiSelectField(
        choices=TOM_ENCRYPTION_CHOICES, max_length=1000, default="", blank=True
    )
    tom_encryption = models.TextField(
        blank=True,
        max_length=2000,
    )
    tom_integrity_selection = MultiSelectField(
        choices=TOM_INTEGRITY_CHOICES, max_length=1000, default="", blank=True
    )
    tom_integrity = models.TextField(
        blank=True,
        max_length=2000,
    )
    tom_availability_selection = MultiSelectField(
        choices=TOM_AVAILABILITY_CHOICES, max_length=1000, default="", blank=True
    )
    tom_availability = models.TextField(
        blank=True,
        max_length=2000,
    )
    tom_evaluation_selection = MultiSelectField(
        choices=TOM_EVALUATION_CHOICES, max_length=1000, default="", blank=True
    )
    tom_evaluation = models.TextField(
        blank=True,
        max_length=2000,
    )
    tom_appropriation_selection = MultiSelectField(
        choices=TOM_APPROPRIATION_CHOICES, max_length=1000, default="", blank=True
    )
    tom_appropriation = models.TextField(
        blank=True,
        max_length=2000,
    )
    tom_transparency_selection = MultiSelectField(
        choices=TOM_TRANSPARENCY_CHOICES, max_length=1000, default="", blank=True
    )
    tom_transparency = models.TextField(
        blank=True,
        max_length=2000,
    )
    tom_subject_rights_selection = MultiSelectField(
        choices=TOM_SUBJECT_RIGHTS_CHOICES, max_length=1000, default="", blank=True
    )
    tom_subject_rights = models.TextField(
        blank=True,
        max_length=2000,
    )
    cname = "TOM"

    class Meta:
        verbose_name = _("Technical and organisational measure")
        verbose_name_plural = _("Technical and organisational measures")

    def __str__(self):
        return f"{self.rpa.slug} {self.cname}"


class RPAAnnex(models.Model):
    """Holds RPA annex list of documents; actual documents need to be
    added manually
    """

    rpa = models.ForeignKey(Rpa, on_delete=models.CASCADE, related_name="rpa_annexes")
    annex_index = models.PositiveSmallIntegerField(
        null=True, choices=list(zip(range(1, 10), range(1, 10)))
    )
    annex_name = models.CharField(max_length=250, blank=True)
    cname = "RPA annex"

    class Meta:
        verbose_name = _("RPA annex")
        verbose_name_plural = _("RPA annexes")
        ordering = ["annex_index"]

    def __str__(self):
        return f"{self.rpa.slug} {self.cname}"

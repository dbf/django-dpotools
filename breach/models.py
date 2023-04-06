"""Breach reporter models"""

from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from multiselectfield import MultiSelectField


class Breach(models.Model):
    """Breach main class; contains breach slug (short name),
    breach_bumper (serves awareness purposes), helptext_display_default
    (help text collapsible box state preset), report_date (supposed not
    to be changed) and report_update (supposed to change to present date
    if updates are made to a breach report); related to
    :model:`auth.User`
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="breaches", null=True
    )
    slug = models.SlugField(
        unique=True,
        max_length=20,
    )
    breach_bumper = models.BooleanField()
    helptext_display_default = models.CharField(
        max_length=20, blank=True, default="show"
    )
    report_date = models.DateField(default=date.today)
    report_update = models.DateField(auto_now=True)

    class Meta:
        verbose_name = _("breach slug")
        verbose_name_plural = _("breach slugs")

    def __str__(self):
        return str(self.slug)


class BreachDataController(models.Model):
    """Stores data controller contact information; related to
    :model:`breach.Breach`
    """

    breach = models.ForeignKey(
        Breach, on_delete=models.CASCADE, related_name="datacontrollers"
    )
    dcon_name = models.CharField(
        max_length=100,
        default=settings.CONTROLLER_NAME,
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
    dcon_email = models.EmailField(
        default=settings.CONTROLLER_EMAIL,
    )
    dcon_reporter = models.CharField(
        max_length=100,
        default=settings.DPO_NAME,
    )
    dcon_reporter_function = models.CharField(
        max_length=100,
        default=settings.DPO_NAME,
    )
    dcon_reporter_email = models.CharField(
        max_length=100,
        default=settings.DPO_EMAIL,
    )
    dcon_reporter_phone = models.CharField(
        max_length=30,
        default=settings.DPO_PHONE,
    )
    dcon_dpo_name = models.CharField(
        max_length=100,
        default=settings.DPO_NAME,
    )
    dcon_dpo_email = models.EmailField(
        default=settings.DPO_EMAIL,
    )
    dcon_dpo_phone = models.CharField(
        max_length=30,
        default=settings.DPO_PHONE,
    )
    dcon_dpo_comment = models.TextField(
        max_length=1000,
        blank=True,
    )
    cname = "data controller"

    class Meta:
        verbose_name = _("Data controller")
        verbose_name_plural = _("Data controllers")

    def __str__(self):
        return f"{self.breach.slug} {self.cname}"

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        self.breach.save()
        return instance


class BreachTimeLine(models.Model):
    """Stores breach time line information; related to
    :model:`breach.Breach`
    """

    YES_NO_CHOICES = [
        ("yes", _("Yes")),
        ("no", _("No")),
    ]

    breach = models.ForeignKey(
        Breach, on_delete=models.CASCADE, related_name="timelines"
    )
    btl_start_known = models.CharField(
        choices=YES_NO_CHOICES,
        max_length=10,
        default="yes",
        blank=False,
    )
    btl_start = models.DateField(blank=True, null=True)
    btl_ongoing = models.CharField(
        choices=YES_NO_CHOICES,
        max_length=10,
        default="yes",
        blank=False,
    )
    btl_end = models.DateField(blank=True, null=True)
    btl_may_recur = models.CharField(
        choices=YES_NO_CHOICES,
        max_length=10,
        default="yes",
        blank=False,
    )
    btl_noticed = models.DateField(blank=True, null=True)
    btl_notif_delay_reason = models.TextField(max_length=1000, blank=True)
    btl_other_supauth = models.TextField(max_length=300, blank=True)
    btl_supauth_od = models.CharField(max_length=500, blank=True)
    btl_remarks = models.TextField(max_length=1000, blank=True)
    btl_dpo_comment = models.TextField(
        max_length=1000,
        blank=True,
    )
    cname = "time line"

    class Meta:
        verbose_name = _("Time line")
        verbose_name_plural = _("Time lines")

    def __str__(self):
        return f"{self.breach.slug} {self.cname}"

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        self.breach.save()
        return instance


class BreachDescription(models.Model):
    """Stores breach description; related to :model:`breach.Breach`"""

    BDESC_CHOICES = [
        (
            "lost_device",
            _("Lost or stolen device (laptop, memory stick, etc.)"),
        ),
        (
            "lost_documents",
            _("Documents lost, stolen or stored in unsafe place"),
        ),
        (
            "lost_postal_mail",
            _("Postal mail lost or accidentally opened"),
        ),
        (
            "unencrypted_email",
            _("Unencrypted email"),
        ),
        (
            "email_cc",
            _("Email with improper CC"),
        ),
        (
            "improperly_disposed_documents",
            _("Improper disposal of documents (records, images, etc.)"),
        ),
        (
            "improperly_disposed_media",
            _(
                "Improper disposal of storage media (hard drives, SSDs, memory sticks, etc.)"
            ),
        ),
        (
            "hacking_phishing",
            _("Hacker attack, malicious software, phishing or similar"),
        ),
        (
            "access_rights_abuse",
            _("Access rights abused (by own employees)"),
        ),
        (
            "accidental_publication",
            _("Accidental publication"),
        ),
        (
            "it_service_wrong_data",
            _("IT service (e.g. Web presence) disclosed false or improper data"),
        ),
    ]
    breach = models.ForeignKey(
        Breach, on_delete=models.CASCADE, related_name="descriptions"
    )
    bdesc_selection = MultiSelectField(
        choices=BDESC_CHOICES, max_length=200, default="", blank=True
    )
    bdesc_selection_other = models.TextField(
        blank=True,
        max_length=300,
    )
    bdesc_description = models.TextField(max_length=2000, blank=True)
    bdesc_dpo_comment = models.TextField(
        max_length=1000,
        blank=True,
    )
    cname = "description"

    class Meta:
        verbose_name = _("Description")
        verbose_name_plural = _("Descriptions")

    def __str__(self):
        return f"{self.breach.slug} {self.cname}"

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        self.breach.save()
        return instance


class BreachAffectedData(models.Model):
    """Stores information regarding data affected by the breach; related
    to :model:`breach.Breach`
    """

    BAFFD_DATA_CHOICES = [
        (
            "not_known_yet",
            _("Not known, yet"),
        ),
        (
            "first_and_last_name",
            _("First and last name"),
        ),
        (
            "date_of_birth",
            _("Date of birth"),
        ),
        (
            "address",
            _("Postal address"),
        ),
        (
            "other_id_data",
            _("Other ID data (ID card number, etc.)"),
        ),
        (
            "localization_data",
            _("Localization data (GPS tracks, etc.)"),
        ),
        (
            "criminal_offense_data",
            _("Data concerning criminal offenses and misdemeanors"),
        ),
        (
            "fiscal_secret",
            _("Data concerning fiscal secrets"),
        ),
        (
            "social_secret",
            _("Data concerning the secrecy of social data"),
        ),
        (
            "professional_secret",
            _("Data concerning professional secrets"),
        ),
        (
            "official_secret",
            _("Data concerning official secrets"),
        ),
    ]

    BAFFD_SPECIAL_DATA_CHOICES = [
        (
            "special_not_known_yet",
            _("Not known, yet"),
        ),
        (
            "ethnic_origin",
            _("Racial or ethnic origin"),
        ),
        (
            "political_opinions",
            _("Political opinions"),
        ),
        (
            "religious_beliefs",
            _("Religious or philosophical beliefs"),
        ),
        (
            "trade_union_membership",
            _("Trade union membership"),
        ),
        (
            "genetic_data",
            _("Genetic data"),
        ),
        (
            "biometric_data",
            _("Biometric data"),
        ),
        (
            "health_data",
            _("Health data"),
        ),
        (
            "sexual_orientation",
            _("Sex life or sexual orientation"),
        ),
    ]

    breach = models.ForeignKey(
        Breach, on_delete=models.CASCADE, related_name="affected_data"
    )
    baffd_selection = MultiSelectField(
        choices=BAFFD_DATA_CHOICES, max_length=200, default="", blank=True
    )
    baffd_selection_other = models.TextField(
        blank=True,
        max_length=300,
    )
    baffd_special_selection = MultiSelectField(
        choices=BAFFD_SPECIAL_DATA_CHOICES, max_length=200, default="", blank=True
    )
    baffd_special_unknown_reason = models.TextField(
        blank=True,
        max_length=500,
    )
    baffd_data_min = models.CharField(
        max_length=150,
        blank=True,
    )
    baffd_data_max = models.CharField(
        max_length=150,
        blank=True,
    )
    baffd_remarks = models.TextField(max_length=1000, blank=True)
    baffd_dpo_comment = models.TextField(
        max_length=1000,
        blank=True,
    )
    cname = "affected data"

    class Meta:
        verbose_name = _("Affected data")
        verbose_name_plural = _("Affected data")

    def __str__(self):
        return f"{self.breach.slug} {self.cname}"

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        self.breach.save()
        return instance


class BreachAffectedSubjects(models.Model):
    """Stores information regarding data subjects (natural persons)
    affected by the breach; related to :model:`breach.Breach`
    """

    BAFFS_DATA_CHOICES = [
        (
            "not_known_yet",
            _("Not known, yet."),
        ),
        (
            "own_employees",
            _("Own employees"),
        ),
        (
            "citizens",
            _("Citizens"),
        ),
        (
            "pupils",
            _("Pupils"),
        ),
        (
            "students",
            _("Students"),
        ),
        (
            "patients",
            _("Patients"),
        ),
        (
            "customers",
            _("Customers"),
        ),
        (
            "minors",
            _("Minors"),
        ),
        (
            "special_protection",
            _("Persons in need of special protection"),
        ),
    ]
    breach = models.ForeignKey(
        Breach, on_delete=models.CASCADE, related_name="affected_subjects"
    )
    baffs_selection = MultiSelectField(
        choices=BAFFS_DATA_CHOICES, max_length=200, default="", blank=True
    )
    baffs_selection_other = models.TextField(
        blank=True,
        max_length=300,
    )
    baffs_datasubjects_min = models.CharField(
        max_length=150,
        blank=True,
    )
    baffs_datasubjects_max = models.CharField(
        max_length=150,
        blank=True,
    )
    baffs_remarks = models.TextField(max_length=1000, blank=True)
    baffs_dpo_comment = models.TextField(
        max_length=1000,
        blank=True,
    )
    cname = "affected subjects"

    class Meta:
        verbose_name = _("Affected subject")
        verbose_name_plural = _("Affected subjects")

    def __str__(self):
        return f"{self.breach.slug} {self.cname}"

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        self.breach.save()
        return instance


class BreachConsequences(models.Model):
    """Stores information regarding likely consequences of the breach
    (for the persons affected, not for the data controller); related to
    :model:`breach.Breach`
    """

    BCONS_CONFIDENTIALITY_CHOICES = [
        (
            "dissemination_to_3rd_party",
            _("Dissemination of data to unauthorized third parties"),
        ),
        (
            "data_linking",
            _("Linking with other data"),
        ),
        (
            "illegitimate_purposes",
            _("Data usage for illegitimate purposes"),
        ),
        (
            "unauthorized_access",
            _("Unauthorized access"),
        ),
    ]
    BCONS_INTEGRITY_CHOICES = [
        (
            "obsolete_data_used",
            _("Obsolete or incorrect data has been used"),
        ),
        (
            "data_falsified",
            _("Data was falsified"),
        ),
        (
            "data_origin_unknown",
            _("Data origin unknown or indeterminate"),
        ),
    ]
    BCONS_AVAILABILITY_CHOICES = [
        (
            "data_unavailable",
            _("Important data is permanently unavailable"),
        ),
        (
            "data_temporarily_unavailable",
            _("Important data was temporarily not available"),
        ),
    ]
    breach = models.ForeignKey(
        Breach, on_delete=models.CASCADE, related_name="consequences"
    )
    bcons_confidentiality_selection = MultiSelectField(
        choices=BCONS_CONFIDENTIALITY_CHOICES, max_length=200, default="", blank=True
    )
    bcons_confidentiality = models.TextField(
        blank=True,
        max_length=300,
    )
    bcons_integrity_selection = MultiSelectField(
        choices=BCONS_INTEGRITY_CHOICES, max_length=200, default="", blank=True
    )
    bcons_integrity = models.TextField(
        blank=True,
        max_length=300,
    )
    bcons_availability_selection = MultiSelectField(
        choices=BCONS_AVAILABILITY_CHOICES, max_length=200, default="", blank=True
    )
    bcons_availability = models.TextField(
        blank=True,
        max_length=300,
    )
    bcons_consequences_descr = models.TextField(
        blank=True,
        max_length=1000,
    )
    bcons_dpo_comment = models.TextField(
        max_length=1000,
        blank=True,
    )
    cname = "consequences"

    class Meta:
        verbose_name = _("Consequence")
        verbose_name_plural = _("Consequences")

    def __str__(self):
        return f"{self.breach.slug} {self.cname}"

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        self.breach.save()
        return instance


class BreachMeasures(models.Model):
    """Stores information regarding measures taken or proposed by the
    controller to address the personal data breach; related to
    :model:`breach.Breach`
    """

    breach = models.ForeignKey(
        Breach, on_delete=models.CASCADE, related_name="measures"
    )
    bmeasures_taken = models.TextField(
        blank=True,
        max_length=2000,
    )

    bmeasures_proposed = models.TextField(
        blank=True,
        max_length=2000,
    )

    bmeasures_no_measures_reason = models.TextField(
        blank=True,
        max_length=2000,
    )
    bmeasures_dpo_comment = models.TextField(
        max_length=1000,
        blank=True,
    )
    cname = "measures"

    class Meta:
        verbose_name = _("Measure")
        verbose_name_plural = _("Measures")

    def __str__(self):
        return f"{self.breach.slug} {self.cname}"

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        self.breach.save()
        return instance


class BreachCommunication(models.Model):
    """Stores information regarding the communication of a personal data
    breach to the data subject(s) (affected persons); related to
    :model:`breach.Breach`
    """

    BCOMM_COMMUNICATION_CHOICES = [
        (
            "already_happened",
            _("Already done (date and details below)."),
        ),
        (
            "not_happened_yet",
            _("Not done, yet, but underway (details below)."),
        ),
        (
            "may_happen",
            _("Is being considered (details below)."),
        ),
        (
            "will_not_happen",
            _("Is not being considered (reason below)."),
        ),
    ]

    BCOMM_MODALITY_CHOICES = [
        (
            "letter",
            _("Letter"),
        ),
        (
            "personal_dialogue",
            _("Personal dialogue"),
        ),
        (
            "publication",
            _("Publication in the media"),
        ),
    ]
    breach = models.ForeignKey(
        Breach, on_delete=models.CASCADE, related_name="communications"
    )
    bcomm_communication_selection = models.CharField(
        choices=BCOMM_COMMUNICATION_CHOICES,
        max_length=100,
        default="already_happened",
        blank=False,
    )
    bcomm_no_communication_reason = models.TextField(
        blank=True,
        max_length=1000,
    )
    bcomm_modality_selection = MultiSelectField(
        choices=BCOMM_MODALITY_CHOICES, max_length=200, default="", blank=True
    )
    bcomm_modality = models.TextField(
        blank=True,
        max_length=300,
    )
    bcomm_number_of_data_subjects = models.CharField(
        max_length=150,
        blank=True,
    )
    bcomm_remarks = models.TextField(max_length=1000, blank=True)
    bcomm_dpo_comment = models.TextField(
        max_length=1000,
        blank=True,
    )
    cname = "communication"

    class Meta:
        verbose_name = _("Communication")
        verbose_name_plural = _("Communications")

    def __str__(self):
        return f"{self.breach.slug} {self.cname}"

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        self.breach.save()
        return instance


class BreachAnnex(models.Model):
    """Stores a single breach annex entry (reference to a breach-related
    document; the actual document needs to be added manually); related
    to :model:`breach.Breach`
    """

    breach = models.ForeignKey(
        Breach, on_delete=models.CASCADE, related_name="breach_annexes"
    )
    bannex_index = models.PositiveSmallIntegerField(
        null=True, choices=list(zip(range(1, 10), range(1, 10)))
    )
    bannex_name = models.CharField(max_length=250, blank=True)
    bannex_dpo_comment = models.TextField(
        max_length=1000,
        blank=True,
    )
    cname = "Breach annex"

    class Meta:
        verbose_name = _("Breach annex")
        verbose_name_plural = _("Breach annexes")
        ordering = ["bannex_index"]

    def __str__(self):
        return f"{self.breach.slug} {self.cname}"

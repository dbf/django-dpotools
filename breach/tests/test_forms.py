from django.test import TestCase
from django.conf import settings

from breach.forms import (
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


class BreachFormTest(TestCase):
    def test_create_breach_new(self):
        """Test whether filling out a new breach form basically works;
        simple form.is_valid() assertion
        """
        form_data = {
            "slug": "testbreach",
            "breach_bumper": True,
            "helptext_display_default": "show",
        }
        form = BreachForm(data=form_data)
        self.assertTrue(form.is_valid())


class BreachDataControllerFormTest(TestCase):
    def test_create_dcon_validation(self):
        """Test whether filling out a new breach data controller form
        basically works; simple form.is_valid() assertion
        """
        form_data = {
            "dcon_name": settings.CONTROLLER_NAME,
            "dcon_street": settings.CONTROLLER_STREET,
            "dcon_pcode": settings.CONTROLLER_PCODE,
            "dcon_city": settings.CONTROLLER_CITY,
            "dcon_email": settings.CONTROLLER_EMAIL,
            "dcon_reporter": settings.DPO_NAME,
            "dcon_reporter_function": settings.DPO_NAME,
            "dcon_reporter_email": settings.DPO_EMAIL,
            "dcon_reporter_phone": settings.DPO_PHONE,
            "dcon_dpo_name": settings.DPO_NAME,
            "dcon_dpo_email": settings.DPO_EMAIL,
            "dcon_dpo_phone": settings.DPO_PHONE,
        }
        form = BreachDataControllerForm(data=form_data)
        self.assertTrue(form.is_valid())


class BreachTimeLineFormTest(TestCase):
    def test_create_btl_validation(self):
        """Test whether filling out a new breach time line form
        basically works; several form.is_valid() assertions
        """
        form_data = {
            "btl_start": "2022-12-06",
            "btl_start_known": "yes",
            "btl_end": "2022-12-07",
            "btl_ongoing": "no",
            "btl_may_recur": "no",
            "btl_noticed": "2022-12-07",
            "btl_notif_delay_reason": "",
            "btl_other_supauth": "",
            "btl_remarks": "",
        }
        form = BreachTimeLineForm(data=form_data)
        self.assertTrue(form.is_valid())
        # 2nd form run
        form_data["btl_start"] = None
        form = BreachTimeLineForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 3rd form run
        form_data["btl_start"] = "2022-12-06"
        form_data["btl_end"] = None
        form = BreachTimeLineForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 4th form run
        form_data["btl_end"] = "2022-12-05"
        form = BreachTimeLineForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 5th form run
        form_data["btl_end"] = "2022-12-07"
        form_data["btl_may_recur"] = None
        form = BreachTimeLineForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 6th form run
        form_data["btl_may_recur"] = "no"
        form_data["btl_noticed"] = None
        form = BreachTimeLineForm(data=form_data)
        self.assertFalse(form.is_valid())


class BreachDescriptionFormTest(TestCase):
    def test_create_bdesc_validation(self):
        """Test whether filling out a new breach description form
        basically works; several form.is_valid() assertions
        """
        form_data = {
            "bdesc_selection": [
                "improperly_disposed_media",
                "accidental_publication",
            ],
            "bdesc_selection_other": "Some other incident",
            "bdesc_description": "Some lengthy breach description",
        }
        form = BreachDescriptionForm(data=form_data)
        self.assertTrue(form.is_valid())
        # 2nd form run
        form_data["bdesc_selection"] = []
        form_data["bdesc_selection_other"] = ""
        form = BreachDescriptionForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 3rd form run
        form_data["bdesc_selection"] = [
            "lost_device",
        ]
        form_data["bdesc_description"] = ""
        form = BreachDescriptionForm(data=form_data)
        self.assertFalse(form.is_valid())


class BreachAffectedDataFormTest(TestCase):
    def test_create_baffd_validation(self):
        """Test whether filling out a new breach affected data form
        basically works; several form.is_valid() assertions
        """
        form_data = {
            "baffd_selection": [
                "other_id_data",
                "official_secret",
            ],
            "baffd_selection_other": "Some other affected data",
            "baffd_special_selection": [
                "political_opinions",
            ],
            "baffd_special_unknown_reason": "",
            "baffd_data_min": "1",
            "baffd_data_max": "approx. 2",
            "baffd_remarks": "Some remarks.",
        }
        form = BreachAffectedDataForm(data=form_data)
        self.assertTrue(form.is_valid())
        # 2nd form run
        form_data["baffd_selection"] = []
        form_data["baffd_selection_other"] = ""
        form = BreachAffectedDataForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 3rd form run
        form_data["baffd_selection_other"] = "Some other affected data"
        form_data["baffd_special_selection"] = [
            "special_not_known_yet",
        ]
        form = BreachAffectedDataForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 4th form run
        form_data["baffd_special_selection"] = [
            "political_opinions",
        ]
        form_data["baffd_data_min"] = ""
        form = BreachAffectedDataForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 5th form run
        form_data["baffd_data_min"] = "1"
        form_data["baffd_data_max"] = ""
        form = BreachAffectedDataForm(data=form_data)
        self.assertFalse(form.is_valid())


class BreachAffectedSubjectsFormTest(TestCase):
    def test_create_baffs_validation(self):
        """Test whether filling out a new breach affected subjects form
        basically works; several form.is_valid() assertions
        """
        form_data = {
            "baffs_selection": [
                "own_employees",
                "patients",
            ],
            "baffs_selection_other": "Some other data subjects",
            "baffs_datasubjects_min": "1",
            "baffs_datasubjects_max": "approx. 2",
            "baffs_remarks": "Some remarks.",
        }
        form = BreachAffectedSubjectsForm(data=form_data)
        self.assertTrue(form.is_valid())
        # 2nd form run
        form_data["baffs_selection"] = []
        form_data["baffs_selection_other"] = ""
        form = BreachAffectedSubjectsForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 3rd form run
        form_data["baffs_selection_other"] = "Some other data subjects"
        form_data["baffs_datasubjects_min"] = ""
        form = BreachAffectedSubjectsForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 4th form run
        form_data["baffs_datasubjects_min"] = "1"
        form_data["baffs_datasubjects_max"] = ""
        form = BreachAffectedSubjectsForm(data=form_data)
        self.assertFalse(form.is_valid())


class BreachConsequencesFormTest(TestCase):
    def test_create_bcons_validation(self):
        """Test whether filling out a new breach consequences form
        basically works; several form.is_valid() assertions
        """
        form_data = {
            "bcons_confidentiality_selection": [
                "illegitimate_purposes",
            ],
            "bcons_confidentiality": "Some other consequences for confidentiality",
            "bcons_integrity_selection": [
                "data_falsified",
            ],
            "bcons_integrity": "Some other consequences for integrity",
            "bcons_availability_selection": [
                "data_unavailable",
            ],
            "bcons_availability": "Some other consequences for availability",
            "bcons_consequences_descr": "Some description of consequences.",
        }
        form = BreachConsequencesForm(data=form_data)
        self.assertTrue(form.is_valid())
        # 2nd form run
        form_data["bcons_confidentiality_selection"] = []
        form_data["bcons_confidentiality"] = ""
        form_data["bcons_integrity_selection"] = []
        form_data["bcons_integrity"] = ""
        form_data["bcons_availability_selection"] = []
        form_data["bcons_availability"] = ""
        form = BreachConsequencesForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 3rd form run
        form_data["bcons_availability_selection"] = [
            "data_unavailable",
        ]
        form_data["bcons_consequences_descr"] = ""
        form = BreachConsequencesForm(data=form_data)
        self.assertFalse(form.is_valid())


class BreachMeasuresFormTest(TestCase):
    def test_create_bmeasures_validation(self):
        """Test whether filling out a new breach measures form basically
        works; several form.is_valid() assertions
        """
        form_data = {
            "bmeasures_taken": "Some measures taken.",
            "bmeasures_proposed": "Some measures proposed.",
            "bmeasures_no_measures_reason": "",
        }
        form = BreachMeasuresForm(data=form_data)
        self.assertTrue(form.is_valid())
        # 2nd form run
        form_data["bmeasures_taken"] = ""
        form_data["bmeasures_proposed"] = ""
        form = BreachMeasuresForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 3rd form run
        form_data["bmeasures_no_measures_reason"] = "Some reason."
        form = BreachMeasuresForm(data=form_data)
        self.assertTrue(form.is_valid())


class BreachCommunicationFormTest(TestCase):
    def test_create_bcomm_validation(self):
        """Test whether filling out a new breach communication form
        basically works; several form.is_valid() assertions
        """
        form_data = {
            "bcomm_communication_selection": "not_happened_yet",
            "bcomm_no_communication_reason": "",
            "bcomm_modality_selection": [
                "letter",
                "personal_dialogue",
            ],
            "bcomm_modality": "Mounted messenger",
            "bcomm_number_of_data_subjects": "approx. 42",
            "bcomm_remarks": "Some remarks.",
        }
        form = BreachCommunicationForm(data=form_data)
        self.assertTrue(form.is_valid())
        # 2nd form run
        form_data["bcomm_communication_selection"] = ""
        form = BreachCommunicationForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 3rd form run
        form_data["bcomm_communication_selection"] = "will_not_happen"
        form = BreachCommunicationForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 4th form run
        form_data["bcomm_no_communication_reason"] = "Some reason for no communication."
        form = BreachCommunicationForm(data=form_data)
        self.assertTrue(form.is_valid())
        # 5th form run
        form_data["bcomm_remarks"] = ""
        form_data["bcomm_communication_selection"] = "already_happened"
        form = BreachCommunicationForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 6th form run
        form_data["bcomm_communication_selection"] = "not_happened_yet"
        form = BreachCommunicationForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 7th form run
        form_data["bcomm_communication_selection"] = "may_happen"
        form = BreachCommunicationForm(data=form_data)
        self.assertFalse(form.is_valid())

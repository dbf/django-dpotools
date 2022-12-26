from django.test import TestCase
from django.conf import settings

from rpa.forms import (
    RpaForm,
    ProcessingActivityNameForm,
    DataControllerForm,
    JointControllerForm,
    DataProtectionOfficerForm,
    InternallyResponsibleDeptForm,
    CategoryOfPersonalDataForm,
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
)


class RpaFormTest(TestCase):
    def test_create_rpa_new(self):
        """Test whether filling out a new RPA form basically works;
        simple form.is_valid() assertion
        """
        form_data = {
            "slug": "satva2022",
            "rpa_bumper": True,
            "helptext_display_default": "show",
        }
        form = RpaForm(data=form_data)
        self.assertTrue(form.is_valid())


class ProcessingActivityNameFormTest(TestCase):
    def test_create_pa_name_new(self):
        """Test whether filling out a new RPA name form basically works;
        simple form.is_valid() assertion (new activity)
        """
        form_data = {
            "name": "Some mildly useful processing activity",
            "is_new": True,
            "date_intro": "2022-11-16",
            "has_changed": None,
            "date_changed": None,
            "former_name": "",
        }
        form = ProcessingActivityNameForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_pa_name_changed(self):
        """Test whether filling out a new RPA name form basically works;
        simple form.is_valid() assertion (changed activity)
        """
        form_data = {
            "name": "Some mildly useful processing activity",
            "is_new": False,
            "date_intro": None,
            "has_changed": True,
            "date_changed": "2022-11-16",
            "former_name": "An even less useful processing activity",
        }
        form = ProcessingActivityNameForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_pa_name_validation(self):
        """Test whether filling out a new RPA name form basically works;
        several form.is_valid() assertions to test form validation
        """
        form_data = {
            "name": "",
            "is_new": False,
            "date_intro": None,
            "has_changed": True,
            "date_changed": "2022-11-16",
            "former_name": "An even less useful processing activity",
        }
        form = ProcessingActivityNameForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 2nd form run
        form_data["name"] = "Some mildly useful processing activity"
        form_data["is_new"] = False
        form_data["has_changed"] = False
        form = ProcessingActivityNameForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 3rd form run
        form_data["is_new"] = True
        form_data["has_changed"] = True
        form = ProcessingActivityNameForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 4th form run
        form_data["is_new"] = None
        form_data["has_changed"] = None
        form = ProcessingActivityNameForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 5th form run
        form_data["is_new"] = None
        form_data["has_changed"] = False
        form = ProcessingActivityNameForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 6th form run
        form_data["is_new"] = False
        form_data["has_changed"] = None
        form = ProcessingActivityNameForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 7th form run
        form_data["is_new"] = True
        form_data["date_intro"] = None
        form = ProcessingActivityNameForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 8th form run
        form_data["is_new"] = None
        form_data["has_changed"] = True
        form_data["date_changed"] = None
        form = ProcessingActivityNameForm(data=form_data)
        self.assertFalse(form.is_valid())


class DataControllerFormTest(TestCase):
    def test_create_dcon_new(self):
        """Test whether filling out a new RPA data controller form
        basically works; simple form.is_valid() assertion
        """
        form_data = {
            "dcon_name": settings.CONTROLLER_NAME,
            "dcon_repby": settings.CONTROLLER_REPBY,
            "dcon_street": settings.CONTROLLER_STREET,
            "dcon_pcode": settings.CONTROLLER_PCODE,
            "dcon_city": settings.CONTROLLER_CITY,
            "dcon_country": settings.CONTROLLER_COUNTRY,
            "dcon_phone": settings.CONTROLLER_PHONE,
            "dcon_email": settings.CONTROLLER_EMAIL,
            "dcon_web": settings.CONTROLLER_WEB,
        }
        form = DataControllerForm(data=form_data)
        self.assertTrue(form.is_valid())


class JointControllerFormTest(TestCase):
    def test_jcon_detail_validation(self):
        """Test whether filling out a new RPA joint controller form
        basically works; several form.is_valid() assertions to test form
        validation
        """
        form_data = {
            "jcon_exists": False,
        }
        form = JointControllerForm(data=form_data)
        self.assertTrue(form.is_valid())
        # 2nd form run
        form_data["jcon_exists"] = None
        form = JointControllerForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 3rd form run
        form_data["jcon_exists"] = True
        form = JointControllerForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 4th form run
        form_data = {
            "jcon_exists": True,
            "jcon_name": "Some other entity",
        }
        form = JointControllerForm(data=form_data)
        self.assertTrue(form.is_valid())


class DataProtectionOfficerFormTest(TestCase):
    def test_create_dpo_new(self):
        """Test whether filling out a new RPA data protection officer
        form basically works; simple form.is_valid() assertion
        """
        form_data = {
            "dpo_name": settings.DPO_NAME,
            "dpo_street": settings.DPO_STREET,
            "dpo_pcode": settings.DPO_PCODE,
            "dpo_city": settings.DPO_CITY,
            "dpo_country": settings.DPO_COUNTRY,
            "dpo_phone": settings.DPO_PHONE,
            "dpo_email": settings.DPO_EMAIL,
            "dpo_web": settings.DPO_WEB,
        }
        form = DataProtectionOfficerForm(data=form_data)
        self.assertTrue(form.is_valid())


class InternallyResponsibleDeptFormTest(TestCase):
    def test_ird_detail_validation(self):
        """Test whether filling out a new RPA internally responsible
        dept. form basically works; several form.is_valid() assertions
        to test form validation
        """
        form_data = {
            "ird_name": "Some dept. of Some Entity",
            "ird_street": "Some Street 42",
            "ird_pcode": "12345",
            "ird_city": "Some City",
            "ird_country": "Some Country",
            "ird_phone": "555-123456",
            "ird_email": "some_dept@subdomain" + settings.CONTROLLER_MAILDOM,
            "ird_comments": "",
        }
        form = InternallyResponsibleDeptForm(data=form_data)
        self.assertTrue(form.is_valid())
        # 2nd form run
        form_data["ird_email"] = "some_dept@some-other-entity.org"
        form = InternallyResponsibleDeptForm(data=form_data)
        self.assertFalse(form.is_valid())


class CategoryOfPersonalDataFormTest(TestCase):
    def test_cpd_detail_validation(self):
        """Test whether filling out a new RPA category of personal data
        form basically works; several form.is_valid() assertions to test
        form validation
        """
        form_data = {
            "cpd_index": 9,
            "cpd_name": "Some category of personal data",
            "cpd_is_special": False,
        }
        form = CategoryOfPersonalDataForm(data=form_data)
        self.assertTrue(form.is_valid())
        # 2nd form run
        form_data["cpd_is_special"] = True
        form = CategoryOfPersonalDataForm(data=form_data)
        self.assertTrue(form.is_valid())
        # 3rd form run
        form_data["cpd_index"] = None
        form = CategoryOfPersonalDataForm(data=form_data)
        self.assertFalse(form.is_valid())


class CategoriesOfPersonalDataOriginFormTest(TestCase):
    def test_cpdo_detail_validation(self):
        """Test whether filling out a new RPA category of personal data
        origin form basically works; several form.is_valid() assertions
        to test form validation
        """
        form_data = {
            "cpdo_descr": "Some description of personal data origin",
        }
        form = CategoriesOfPersonalDataOriginForm(data=form_data)
        self.assertTrue(form.is_valid())
        # 2nd form run
        form_data["cpdo_descr"] = ""
        form = CategoriesOfPersonalDataOriginForm(data=form_data)
        self.assertFalse(form.is_valid())


class PurposeAndLegalBasisFormTest(TestCase):
    def test_create_plb_new(self):
        """Test whether filling out a new RPA purpose and legal basis
        form basically works; simple form.is_valid() assertion
        """
        form_data = {
            "plb_purpose": "Some description of processing activity purpose",
            "plb": [
                "plb_art6_1a",
            ],
            "plb_reasons": "Some explanation of choice for legal bases",
        }
        form = PurposeAndLegalBasisForm(data=form_data)
        self.assertTrue(form.is_valid())


class DataSubjectFormTest(TestCase):
    def test_dsub_detail_validation(self):
        """Test whether filling out a new RPA data subject form
        basically works; several form.is_valid() assertions to test form
        validation
        """
        form_data = {
            "dsub_name": "Some data subject category",
            "dsub_cpd_sel": [
                "1",
                "2",
            ],
        }
        form = DataSubjectForm(data=form_data)
        self.assertTrue(form.is_valid())
        # 2nd form run
        form_data["dsub_name"] = ""
        form = DataSubjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 3rd form run
        form_data["dsub_name"] = "Some data subject category"
        form_data["dsub_cpd_sel"] = []
        form = DataSubjectForm(data=form_data)
        self.assertFalse(form.is_valid())


class TimeLimitForErasureFormTest(TestCase):
    def test_create_tle_new(self):
        """Test whether filling out a new RPA time limits for erasure
        form basically works; simple form.is_valid() assertion
        """
        form_data = {
            "tle_handling": "tle_in_rpa",
            "tle_start": "Some start description.",
            "tle_length": "Some length description.",
            "tle_comment": "Some comment.",
            "tle_cpd_sel": [
                "1",
                "2",
            ],
        }
        form = TimeLimitForErasureForm(data=form_data)
        self.assertTrue(form.is_valid())


class CategoryOfRecipientsFormTest(TestCase):
    def test_create_crec_new(self):
        """Test whether filling out a new RPA category of recipients
        form basically works; simple form.is_valid() assertion
        """
        form_data = {
            "crec_handling": "crec_in_rpa",
            "crec_designation": "Some category of recipients.",
            "crec_is_external": False,
            "crec_cpd_sel": [
                "1",
                "2",
            ],
        }
        form = CategoryOfRecipientsForm(data=form_data)
        self.assertTrue(form.is_valid())


class TransferToThirdCountryFormTest(TestCase):
    def test_ttc_detail_validation(self):
        """Test whether filling out a new RPA transfer to third country
        form basically works; several form.is_valid() assertions to test
        form validation
        """
        form_data = {
            "ttc_3rdcountry_intended": True,
            "ttc_3rdcountry": "Some 3rd country recipient.",
            "ttc_3rdcountry_adequacy": False,
            "ttc_non_adequacy_choices": [
                "ttc_sdpc",
            ],
            "ttc_non_adequacy_explanation": "Some explanation.",
        }
        form = TransferToThirdCountryForm(data=form_data)
        self.assertTrue(form.is_valid())
        # 2nd form run
        form_data["ttc_3rdcountry_intended"] = None
        form = TransferToThirdCountryForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 3rd form run
        form_data["ttc_3rdcountry_intended"] = True
        form_data["ttc_3rdcountry"] = ""
        form = TransferToThirdCountryForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 4th form run
        form_data["ttc_3rdcountry"] = "Some 3rd country recipient."
        form_data["ttc_3rdcountry_adequacy"] = None
        form = TransferToThirdCountryForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 5th form run
        form_data["ttc_3rdcountry_adequacy"] = False
        form_data["ttc_non_adequacy_choices"] = [
            "ttc_sdpc",
        ]
        form_data["ttc_non_adequacy_explanation"] = ""
        form = TransferToThirdCountryForm(data=form_data)
        self.assertFalse(form.is_valid())


class AccessGroupFormTest(TestCase):
    def test_create_agrp_new(self):
        """Test whether filling out a new RPA access group form
        basically works; simple form.is_valid() assertion
        """
        form_data = {
            "agrp_handling": "agrp_in_rpa",
            "agrp_name": "Some access group.",
            "agrp_can_read": True,
            "agrp_can_edit": True,
            "agrp_can_delete": True,
            "agrp_cpd_sel": [
                "1",
                "2",
            ],
        }
        form = AccessGroupForm(data=form_data)
        self.assertTrue(form.is_valid())


class TransparencyFormTest(TestCase):
    def test_tran_detail_validation(self):
        """Test whether filling out a new RPA transparency form
        basically works; several form.is_valid() assertions to test form
        validation
        """
        form_data = {
            "tran_choices": [
                "tran_leaflet",
                "tran_online",
            ],
            "tran_explanation": "Some explanation.",
        }
        form = TransparencyForm(data=form_data)
        self.assertTrue(form.is_valid())
        # 2nd form run
        form_data["tran_choices"] = []
        form = TransparencyForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 3rd form run
        form_data["tran_choices"] = [
            "tran_leaflet",
            "tran_online",
        ]
        form_data["tran_explanation"] = ""
        form = TransparencyForm(data=form_data)
        self.assertFalse(form.is_valid())


class DataProcessorFormTest(TestCase):
    def test_dpro_detail_validation(self):
        """Test whether filling out a new RPA data processor form
        basically works; several form.is_valid() assertions to test form
        validation
        """
        form_data = {
            "dpro_is_assigned": True,
            "dpro_name": "Some DP name.",
            "dpro_street": "Some DP street.",
            "dpro_pcode": "12345",
            "dpro_city": "Some DP city.",
            "dpro_country": "Some DP country.",
            "dpro_contact": "Some contact at DP.",
        }
        form = DataProcessorForm(data=form_data)
        self.assertTrue(form.is_valid())
        # 2nd form run
        form_data["dpro_is_assigned"] = None
        form = DataProcessorForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 3rd form run
        form_data["dpro_is_assigned"] = True
        form_data["dpro_name"] = ""
        form = DataProcessorForm(data=form_data)
        self.assertFalse(form.is_valid())


class PrivacyImpactAssessmentFormTest(TestCase):
    def test_pia_detail_validation(self):
        """Test whether filling out a new RPA PIA form basically works;
        several form.is_valid() assertions to test form validation
        """
        form_data = {
            "pia_required": True,
            "pia_not_required_reason": [],
            "pia_results": [
                "pia_additional_measures",
            ],
        }
        form = PrivacyImpactAssessmentForm(data=form_data)
        self.assertTrue(form.is_valid())
        # 2nd form run
        form_data["pia_required"] = None
        form = PrivacyImpactAssessmentForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 3rd form run
        form_data["pia_required"] = True
        form_data["pia_results"] = []
        form = PrivacyImpactAssessmentForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 4th form run
        form_data["pia_required"] = False
        form_data["pia_not_required_reason"] = []
        form = PrivacyImpactAssessmentForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 5th form run
        form_data["pia_not_required_reason"] = [
            "pia_nr_automated_processing",
            "pia_nr_special_categories",
            "pia_nr_monitoring_public",
        ]
        form = PrivacyImpactAssessmentForm(data=form_data)
        self.assertFalse(form.is_valid())


class TOMFormTest(TestCase):
    def test_tom_detail_validation(self):
        """Test whether filling out a new RPA TOM form basically works;
        several form.is_valid() assertions to test form validation
        """
        form_data = {
            "tom_handling": "tom_in_rpa",
            "tom_pseudonym_selection": [],
            "tom_pseudonym": "Some measures regarding pseudonymization.",
            "tom_encryption_selection": [],
            "tom_encryption": "Some measures regarding encryption.",
            "tom_integrity_selection": [],
            "tom_integrity": "Some measures regarding integrity/confidentiality.",
            "tom_availability_selection": [],
            "tom_availability": "Some measures regarding availability/resilience.",
            "tom_evaluation_selection": [],
            "tom_evaluation": "Some measures regarding evaluation.",
            "tom_appropriation_selection": [],
            "tom_appropriation": "Some measures regarding appropriation.",
            "tom_transparency_selection": [],
            "tom_transparency": "Some measures regarding transparency.",
            "tom_subject_rights_selection": [],
            "tom_subject_rights": "Some measures regarding subject rights.",
        }
        form = TOMForm(data=form_data)
        self.assertTrue(form.is_valid())
        # 2nd form run
        form_data["tom_handling"] = ""
        form = TOMForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 3rd form run
        form_data["tom_handling"] = "tom_in_rpa"
        form_data["tom_pseudonym"] = ""
        form = TOMForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 4th form run
        form_data["tom_pseudonym"] = "Some measures regarding pseudonymization."
        form_data["tom_encryption"] = ""
        form = TOMForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 5th form run
        form_data["tom_encryption"] = "Some measures regarding encryption."
        form_data["tom_integrity"] = ""
        form = TOMForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 6th form run
        form_data[
            "tom_integrity"
        ] = "Some measures regarding integrity/confidentiality."
        form_data["tom_availability"] = ""
        form = TOMForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 7th form run
        form_data[
            "tom_availability"
        ] = "Some measures regarding availability/resilience."
        form_data["tom_evaluation"] = ""
        form = TOMForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 8th form run
        form_data["tom_evaluation"] = "Some measures regarding evaluation."
        form_data["tom_appropriation"] = ""
        form = TOMForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 9th form run
        form_data["tom_appropriation"] = "Some measures regarding appropriation."
        form_data["tom_transparency"] = ""
        form = TOMForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 10th form run
        form_data["tom_transparency"] = "Some measures regarding transparency."
        form_data["tom_subject_rights"] = ""
        form = TOMForm(data=form_data)
        self.assertFalse(form.is_valid())


class RPAAnnexFormTest(TestCase):
    def test_create_annex_new(self):
        """Test whether filling out a new RPA annex form basically
        works; simple form.is_valid() assertion
        """
        form_data = {
            "annex_index": 4,
            "annex_name": "Some annex.",
        }
        form = RPAAnnexForm(data=form_data)
        self.assertTrue(form.is_valid())

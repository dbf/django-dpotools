from django_webtest import WebTest

from rpa.models import (
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


class RPADeleteViewTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-empty-kuno.json",
    ]

    def test_delete_confirm_cancel_myrpas(self):
        """Test whether users can delete their own RPAs from myrpas list
        and whether cancelling the deletion confirmation works.
        """
        ownrpa = Rpa.objects.get(pk="1")
        deletepage = self.app.get(
            "/rpa/myrpas/detail/" + ownrpa.slug + "/delete/", user="kuno"
        )
        form = deletepage.forms["delete-confirmation"]
        form.submit("cancel", value="Cancel")
        assert deletepage.status_int == 200
        assert Rpa.objects.exists() is True
        form.submit(value="Confirm")
        assert deletepage.status_int == 200
        assert Rpa.objects.exists() is False


class AllRPADeleteViewTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-empty-kuno.json",
    ]

    def test_delete_confirm_cancel_allrpas(self):
        """Test whether dpo user can delete RPAs from allrpas list and
        whether cancelling the deletion confirmation works.
        """
        otherrpa = Rpa.objects.get(pk="1")
        deletepage = self.app.get(
            "/rpa/allrpas/detail/" + otherrpa.slug + "/delete/", user="hugo"
        )
        form = deletepage.forms["delete-confirmation"]
        form.submit("cancel", value="Cancel")
        assert deletepage.status_int == 200
        assert Rpa.objects.exists() is True
        form.submit(value="Confirm")
        assert deletepage.status_int == 200
        assert Rpa.objects.exists() is False


class RPACreateRpanmViewTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete.json",
    ]

    def test_rpanm_template_details(self):
        """Test rpanm changed activity to please coverage for
        commontemplate."
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/rpanm/", user="kuno"
        )
        form = editpage.forms["edit-rpanm"]
        form["is_new"] = "false"
        form["has_changed"] = "true"
        form["date_changed"] = "2022-12-15"
        form["former_name"] = "Some former name"
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert ProcessingActivityName.objects.exists() is True
        detail_view = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/", user="kuno"
        )
        assert ("Modified processing activity" in detail_view) is True
        assert ("Date changed" in detail_view) is True
        assert ("Former name of processing activity" in detail_view) is True


class RPACreateDconViewTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete.json",
    ]

    def test_update_dcon(self):
        """Test whether a DataController model instance can be
        successfully updated (just re-save, since data is read-only).
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/dcon/", user="kuno"
        )
        form = editpage.forms["edit-dcon"]
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert DataController.objects.exists() is True
        rpadcon = DataController.objects.filter().first()
        assert rpadcon.dcon_name == "Some entity"


class RPACreateJconViewTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete.json",
    ]

    def test_update_jcon(self):
        """Test whether a JointController model instance can be
        successfully updated.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/jcon/", user="kuno"
        )
        form = editpage.forms["edit-jcon"]
        form["jcon_exists"] = "true"
        form["jcon_name"] = "Some joint controller"
        form["jcon_contact"] = "Some contact person at the joint controller"
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert JointController.objects.exists() is True
        rpajcon = JointController.objects.filter().first()
        assert rpajcon.jcon_name == "Some joint controller"
        detail_view = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/", user="kuno"
        )
        soup = detail_view.html
        jcon_data = soup.find(id="info-jcon").get_text()
        assert ("Joint controller - Name" in jcon_data) is True
        assert ("Joint controller - Contact person" in jcon_data) is True

    def test_update_jcon_with_empty_jcon_name(self):
        """Test whether a JointController model instance update
        will fail with empty jcon_name.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/jcon/", user="kuno"
        )
        form = editpage.forms["edit-jcon"]
        form["jcon_exists"] = "true"
        form["jcon_name"] = ""
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("please enter their contact data" in res) is True


class RPACreateDpoViewTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete.json",
    ]

    def test_update_dpo(self):
        """Test whether a DataProtectionOfficer model instance can be
        successfully updated (just re-save, since data is read-only).
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/dpo/", user="kuno"
        )
        form = editpage.forms["edit-dpo"]
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert DataProtectionOfficer.objects.exists() is True
        rpadpo = DataProtectionOfficer.objects.filter().first()
        assert rpadpo.dpo_name == "Data Protection Officer"


class RPACreateIrdViewTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete.json",
    ]

    def test_update_ird(self):
        """Test whether a InternallyResponsibleDept model instance can be
        successfully updated.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/ird/", user="kuno"
        )
        form = editpage.forms["edit-ird"]
        form["ird_name"] = "Some internally reponsible dept."
        form["ird_email"] = "some_dept@depts.some-entity.org"
        form["ird_comments"] = "Some comments."
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert InternallyResponsibleDept.objects.exists() is True
        rpaird = InternallyResponsibleDept.objects.filter().first()
        assert rpaird.ird_email == "some_dept@depts.some-entity.org"
        detail_view = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/", user="kuno"
        )
        soup = detail_view.html
        ird_data = soup.find(id="info-ird").get_text()
        assert ("Processing Dept. - Name" in ird_data) is True
        assert ("Processing Dept. - E-mail" in ird_data) is True
        assert ("Processing Dept. - Comments" in ird_data) is True

    def test_update_ird_with_wrong_ird_email(self):
        """Test whether a InternallyResponsibleDept model instance update
        will fail with wrong email.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/ird/", user="kuno"
        )
        form = editpage.forms["edit-ird"]
        form["ird_email"] = "some_dept@some-other-entity.org"
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("Please enter a valid Email address" in res) is True


class RPACreateCpdViewTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete.json",
    ]

    def test_update_cpd(self):
        """Test whether a CategoryOfPersonalData model instance can be
        successfully updated.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/cpd/", user="kuno"
        )
        form = editpage.forms["edit-cpd"]
        form["form-0-cpd_index"] = 1
        form["form-0-cpd_name"] = "Full name"
        form["form-0-cpd_is_special"] = False
        form["form-1-cpd_index"] = 2
        form["form-1-cpd_name"] = "Email address"
        form["form-1-cpd_is_special"] = False
        form["form-2-cpd_index"] = 3
        form["form-2-cpd_name"] = "Philosophical beliefs"
        form["form-2-cpd_is_special"] = True
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert CategoryOfPersonalData.objects.exists() is True
        rpacpd = CategoryOfPersonalData.objects.filter(cpd_index=3).get()
        assert rpacpd.cpd_name == "Philosophical beliefs"

    def test_update_cpd_with_index_already_in_use(self):
        """Test whether a CategoryOfPersonalData model instance update
        will fail with cpd_index already in use.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/cpd/", user="kuno"
        )
        form = editpage.forms["edit-cpd"]
        form["form-0-cpd_index"] = 1
        form["form-0-cpd_name"] = "Full name"
        form["form-0-cpd_is_special"] = False
        form["form-1-cpd_index"] = 1
        form["form-1-cpd_name"] = "Email address"
        form["form-1-cpd_is_special"] = False
        form["form-2-cpd_index"] = 3
        form["form-2-cpd_name"] = "Philosophical beliefs"
        form["form-2-cpd_is_special"] = True
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("Index already in use" in res) is True

    def test_update_cpd_with_empty_cpd_name(self):
        """Test whether a CategoryOfPersonalData model instance update
        will fail with empty cpd_name.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/cpd/", user="kuno"
        )
        form = editpage.forms["edit-cpd"]
        form["form-0-cpd_index"] = 1
        form["form-0-cpd_name"] = "Full name"
        form["form-0-cpd_is_special"] = False
        form["form-1-cpd_index"] = 2
        form["form-1-cpd_name"] = "Email address"
        form["form-1-cpd_is_special"] = False
        form["form-2-cpd_index"] = 3
        form["form-2-cpd_name"] = ""
        form["form-2-cpd_is_special"] = True
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("Category of personal data missing" in res) is True


class RPACreateCpdoViewTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete.json",
    ]

    def test_update_cpdo(self):
        """Test whether a CategoriesOfPersonalDataOrigin model instance
        can be successfully updated.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/cpdo/", user="kuno"
        )
        form = editpage.forms["edit-cpdo"]
        form["cpdo_descr"] = "Some other data source"
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert CategoriesOfPersonalDataOrigin.objects.exists() is True
        rpacpdo = CategoriesOfPersonalDataOrigin.objects.filter().first()
        assert rpacpdo.cpdo_descr == "Some other data source"

    def test_update_cpdo_with_empty_cpdo_descr(self):
        """Test whether a CategoriesOfPersonalDataOrigin model instance
        update will fail with empty cpdo_descr.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/cpdo/", user="kuno"
        )
        form = editpage.forms["edit-cpdo"]
        form["cpdo_descr"] = ""
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("give a brief description of the origin" in res) is True


class RPACreatePlbViewTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete.json",
    ]

    def test_update_plb(self):
        """Test whether a PurposeAndLegalBasis model instance can be
        successfully updated.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/plb/", user="kuno"
        )
        form = editpage.forms["edit-plb"]
        form["plb_purpose"] = "Some other purpose."
        form["plb"] = [
            "plb_art6_1e",
        ]
        form["plb_reasons"] = "Some other explanation."
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert PurposeAndLegalBasis.objects.exists() is True
        rpaplb = PurposeAndLegalBasis.objects.filter().first()
        assert rpaplb.plb_purpose == "Some other purpose."

    def test_update_plb_with_empty_plb_purpose(self):
        """Test whether a PurposeAndLegalBasis model instance update
        will fail with empty plb_purpose.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/plb/", user="kuno"
        )
        form = editpage.forms["edit-plb"]
        form["plb_purpose"] = ""
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("This field is required" in res) is True
        form["plb_purpose"] = "Some other purpose."
        form["plb"] = []
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("This field is required" in res) is True
        form["plb"] = [
            "plb_art6_1e",
        ]
        form["plb_reasons"] = ""
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("This field is required" in res) is True


class RPACreateDSubViewTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete.json",
    ]

    def test_update_dsub(self):
        """Test whether a DataSubject model instance can be
        successfully updated.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/dsub/", user="kuno"
        )
        form = editpage.forms["edit-dsub"]
        form["form-0-dsub_cpd_sel"] = [1, 2, 3]
        form["form-1-dsub_name"] = "Emeriti"
        form["form-1-dsub_cpd_sel"] = [1, 3]
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert DataSubject.objects.exists() is True

        rpadsub = DataSubject.objects.filter(dsub_name="Emeriti").prefetch_related(
            "cpd"
        )
        rpadsub_cpd = CategoryOfPersonalData.objects.filter(datasubjects__in=rpadsub)
        expected_dsub_cpd = "1 3"
        actual_dsub_cpd = (
            str(rpadsub_cpd[0].cpd_index) + " " + str(rpadsub_cpd[1].cpd_index)
        )
        assert actual_dsub_cpd == expected_dsub_cpd

    def test_update_dsub_with_empty_cpd_name(self):
        """Test whether a DataSubject model instance update
        will fail with no cpd given.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/dsub/", user="kuno"
        )
        form = editpage.forms["edit-dsub"]
        form["form-2-dsub_name"] = "Alumni"
        form["form-2-dsub_cpd_sel"] = []
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("You must fill in the categories of personal data" in res) is True


class RPACreateTleViewTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete.json",
    ]

    def test_update_tle_with_empty_tle_start(self):
        """Test whether a TimeLimitForErasure model instance update
        will fail with no tle_start given.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/tle/", user="kuno"
        )
        form = editpage.forms["edit-tle"]
        form["form-0-tle_handling"] = ""
        form["form-0-tle_start"] = "Some tle start"
        form["form-0-tle_length"] = "Some tle length"
        form["form-0-tle_comment"] = "Some tle comment"
        form["form-0-tle_cpd_sel"] = [
            1,
        ]
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("Select how to state your time limits for erasure" in res) is True
        form["form-0-tle_handling"] = "tle_in_rpa"
        form["form-0-tle_start"] = ""
        form["form-0-tle_length"] = "Some tle length"
        form["form-0-tle_comment"] = "Some tle comment"
        form["form-0-tle_cpd_sel"] = [
            1,
        ]
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert (
            "At least one time limit for erasure (start and length) is required" in res
        ) is True
        form["form-0-tle_start"] = "Some tle start"
        form["form-0-tle_length"] = ""
        form["form-0-tle_comment"] = "Some tle comment"
        form["form-0-tle_cpd_sel"] = [
            1,
        ]
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert (
            "At least one time limit for erasure (start and length) is required" in res
        ) is True
        form["form-0-tle_start"] = "Some tle start"
        form["form-0-tle_length"] = "Some tle length"
        form["form-0-tle_comment"] = ""
        form["form-0-tle_cpd_sel"] = [
            1,
        ]
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("Please state a reason for this time limit for erasure" in res) is True
        form["form-0-tle_start"] = "Some tle start"
        form["form-0-tle_length"] = "Some tle length"
        form["form-0-tle_comment"] = "Some tle comment"
        form["form-0-tle_cpd_sel"] = []
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("You must fill in the categories of personal data" in res) is True

    def test_update_tle(self):
        """Test whether a TimeLimitForErasure model instance can be
        successfully updated.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/tle/", user="kuno"
        )
        form = editpage.forms["edit-tle"]
        form["form-0-tle_handling"] = "tle_in_rpa"
        form["form-0-tle_start"] = "Some tle start"
        form["form-0-tle_length"] = "Some tle length"
        form["form-0-tle_comment"] = "Some tle comment"
        form["form-0-tle_cpd_sel"] = [2, 3]
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert TimeLimitForErasure.objects.exists() is True

        rpatle = TimeLimitForErasure.objects.filter(
            tle_comment="Some tle comment"
        ).prefetch_related("cpd")
        rpatle_cpd = CategoryOfPersonalData.objects.filter(timelimits__in=rpatle)
        expected_tle_cpd = "2 3"
        actual_tle_cpd = (
            str(rpatle_cpd[0].cpd_index) + " " + str(rpatle_cpd[1].cpd_index)
        )
        assert actual_tle_cpd == expected_tle_cpd
        detail_view = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/", user="kuno"
        )
        soup = detail_view.html
        tle_data = soup.find(id="info-tle").get_text()
        assert ("Time limit start" in tle_data) is True
        assert ("Time limit length" in tle_data) is True
        assert ("Comment" in tle_data) is True
        assert ("Applies to data categories:" in tle_data) is True


class RPACreateCrecViewTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete.json",
    ]

    def test_update_crec_with_empty_crec_designation(self):
        """Test whether a CategoryOfRecipients model instance update
        will fail with no crec_start given.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/crec/", user="kuno"
        )
        form = editpage.forms["edit-crec"]
        form["form-0-crec_handling"] = ""
        form["form-0-crec_designation"] = "Some category of recipients"
        form["form-0-crec_is_external"] = "false"
        form["form-0-crec_cpd_sel"] = [
            1,
        ]
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert (
            "do you intend to transfer personal data to some person or entity" in res
        ) is True
        form["form-0-crec_handling"] = "crec_in_rpa"
        form["form-0-crec_designation"] = ""
        form["form-0-crec_is_external"] = "false"
        form["form-0-crec_cpd_sel"] = [
            1,
        ]
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("If you intend to transfer personal data, you must" in res) is True
        form["form-0-crec_handling"] = "crec_in_rpa"
        form["form-0-crec_designation"] = "Some category of recipients"
        form["form-0-crec_is_external"] = "unknown"
        form["form-0-crec_cpd_sel"] = [
            1,
        ]
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("Is this recipient an external recipient?" in res) is True
        form["form-0-crec_handling"] = "crec_in_rpa"
        form["form-0-crec_designation"] = "Some category of recipients"
        form["form-0-crec_is_external"] = "false"
        form["form-0-crec_cpd_sel"] = []
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert (
            "you must fill in the affected categories of personal data" in res
        ) is True

    def test_update_crec(self):
        """Test whether a CategoryOfRecipients model instance can be
        successfully updated.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/crec/", user="kuno"
        )
        form = editpage.forms["edit-crec"]
        form["form-0-crec_handling"] = "crec_in_annex"
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert CategoryOfRecipients.objects.exists() is True
        detail_view = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/", user="kuno"
        )
        soup = detail_view.html
        crecannex = soup.find(id="info-crec").get_text()
        assert (
            "A list of categories of recipients that covers all categories of"
            in crecannex
        ) is True
        form = editpage.forms["edit-crec"]
        form["form-0-crec_handling"] = "crec_in_rpa"
        form["form-0-crec_designation"] = "Some other category of recipients"
        form["form-0-crec_is_external"] = "true"
        form["form-0-crec_cpd_sel"] = [1, 2]
        form["form-1-crec_designation"] = "Some different category of recipients"
        form["form-1-crec_is_external"] = "false"
        form["form-1-crec_cpd_sel"] = [2, 3]
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert CategoryOfRecipients.objects.exists() is True
        rpacrec = CategoryOfRecipients.objects.filter(
            crec_designation="Some other category of recipients"
        ).prefetch_related("cpd")
        rpacrec_cpd = CategoryOfPersonalData.objects.filter(recipients__in=rpacrec)
        expected_crec_cpd = "1 2"
        actual_crec_cpd = (
            str(rpacrec_cpd[0].cpd_index) + " " + str(rpacrec_cpd[1].cpd_index)
        )
        assert actual_crec_cpd == expected_crec_cpd
        detail_view = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/", user="kuno"
        )
        soup = detail_view.html
        crec_data = soup.find(id="info-crec").get_text()
        assert ("Internal recipient contact data" in crec_data) is True
        assert ("External recipient contact data" in crec_data) is True
        assert ("Applies to data categories:" in crec_data) is True


class RPACreateTtcViewTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete.json",
    ]

    def test_update_ttc_with_empty_ttc_3rdcountry(self):
        """Test whether a TransferToThirdCountry model instance update
        will fail with empty ttc_3rdcountry.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/ttc/", user="kuno"
        )
        form = editpage.forms["edit-ttc"]
        form["ttc_3rdcountry_intended"] = "unknown"
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert (
            "Do you intend to transfer personal data to a third country or an" in res
        ) is True
        form["ttc_3rdcountry_intended"] = "true"
        form["ttc_3rdcountry"] = ""
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("you must fill in the recipients" in res) is True
        form["ttc_3rdcountry_intended"] = "true"
        form["ttc_3rdcountry"] = "Some recipient in some third country"
        form["ttc_3rdcountry_adequacy"] = "unknown"
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert (
            "Is there an adequacy decision for your intended transfer" in res
        ) is True
        form["ttc_3rdcountry_intended"] = "true"
        form["ttc_3rdcountry"] = "Some recipient in some third country"
        form["ttc_3rdcountry_adequacy"] = "false"
        form["ttc_non_adequacy_choices"] = []
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("you must choose at least one exception" in res) is True
        form["ttc_3rdcountry_intended"] = "true"
        form["ttc_3rdcountry"] = "Some recipient in some third country"
        form["ttc_3rdcountry_adequacy"] = "false"
        form["ttc_non_adequacy_choices"] = [
            "ttc_sdpc",
        ]
        form["ttc_non_adequacy_explanation"] = ""
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("explain the exception you chose" in res) is True

    def test_update_ttc(self):
        """Test whether a TransferToThirdCountry model instance can be
        successfully updated.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/ttc/", user="kuno"
        )
        form = editpage.forms["edit-ttc"]
        form["ttc_3rdcountry_intended"] = "true"
        form["ttc_3rdcountry"] = "Some US mega corp."
        form["ttc_3rdcountry_adequacy"] = "false"
        form["ttc_non_adequacy_choices"] = [
            "ttc_sdpc",
        ]
        form["ttc_non_adequacy_explanation"] = "Some blatant nonsense explanation"
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert TransferToThirdCountry.objects.exists() is True
        rpattc = TransferToThirdCountry.objects.filter().first()
        assert (
            rpattc.ttc_non_adequacy_explanation == "Some blatant nonsense explanation"
        )
        detail_view = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/", user="kuno"
        )
        assert ("Third country recipients adequacy" in detail_view) is True
        assert ("Non-adequacy exception choices" in detail_view) is True
        assert (
            "Explanation for choice of non-adequacy exception" in detail_view
        ) is True
        form = editpage.forms["edit-ttc"]
        form["ttc_3rdcountry_intended"] = "true"
        form["ttc_3rdcountry"] = "Some recipient in some third country"
        form["ttc_3rdcountry_adequacy"] = "true"
        res = form.submit(value="Submit")
        assert res.status_int == 302
        detail_view = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/", user="kuno"
        )
        soup = detail_view.html
        adequacy = soup.find(id="info-ttc").get_text()
        assert ("Third country recipients adequacy\nyes" in adequacy) is True


class RPACreateAgrpViewTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete.json",
    ]

    def test_update_agrp_with_empty_agrp_name(self):
        """Test whether a AccessGroup model instance update will fail
        with no agrp_name given.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/agrp/", user="kuno"
        )
        form = editpage.forms["edit-agrp"]
        form["form-0-agrp_handling"] = ""
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("Select how to state access groups for this RPA" in res) is True
        form["form-0-agrp_handling"] = "agrp_in_rpa"
        form["form-0-agrp_name"] = ""
        form["form-0-agrp_can_read"] = "true"
        form["form-0-agrp_can_edit"] = "true"
        form["form-0-agrp_can_delete"] = "true"
        form["form-0-agrp_cpd_sel"] = [
            1,
        ]
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("At least one access group must be named" in res) is True
        form["form-0-agrp_handling"] = "agrp_in_rpa"
        form["form-0-agrp_name"] = "Some access group"
        form["form-0-agrp_can_read"] = "unknown"
        form["form-0-agrp_can_edit"] = "true"
        form["form-0-agrp_can_delete"] = "true"
        form["form-0-agrp_cpd_sel"] = [
            1,
        ]
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("for this access group must each be either" in res) is True
        form["form-0-agrp_handling"] = "agrp_in_rpa"
        form["form-0-agrp_name"] = "Some access group"
        form["form-0-agrp_can_read"] = "true"
        form["form-0-agrp_can_edit"] = "unknown"
        form["form-0-agrp_can_delete"] = "true"
        form["form-0-agrp_cpd_sel"] = [
            1,
        ]
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("for this access group must each be either" in res) is True
        form["form-0-agrp_handling"] = "agrp_in_rpa"
        form["form-0-agrp_name"] = "Some access group"
        form["form-0-agrp_can_read"] = "true"
        form["form-0-agrp_can_edit"] = "true"
        form["form-0-agrp_can_delete"] = "unknown"
        form["form-0-agrp_cpd_sel"] = [
            1,
        ]
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("for this access group must each be either" in res) is True
        form["form-0-agrp_handling"] = "agrp_in_rpa"
        form["form-0-agrp_name"] = "Some access group"
        form["form-0-agrp_can_read"] = "false"
        form["form-0-agrp_can_edit"] = "false"
        form["form-0-agrp_can_delete"] = "false"
        form["form-0-agrp_cpd_sel"] = [
            1,
        ]
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert (
            "An access group with no access rights does not make sense" in res
        ) is True
        form["form-0-agrp_handling"] = "agrp_in_rpa"
        form["form-0-agrp_name"] = "Some access group"
        form["form-0-agrp_can_read"] = "true"
        form["form-0-agrp_can_edit"] = "true"
        form["form-0-agrp_can_delete"] = "true"
        form["form-0-agrp_cpd_sel"] = []
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("You must fill in the categories of personal data" in res) is True

    def test_update_agrp(self):
        """Test whether a AccessGroup model instance can be successfully
        updated.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/agrp/", user="kuno"
        )
        form = editpage.forms["edit-agrp"]
        form["form-0-agrp_handling"] = "agrp_in_rpa"
        form["form-0-agrp_name"] = "Some other access group"
        form["form-0-agrp_can_read"] = "true"
        form["form-0-agrp_can_edit"] = "true"
        form["form-0-agrp_can_delete"] = "true"
        form["form-0-agrp_cpd_sel"] = [1, 3]
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert AccessGroup.objects.exists() is True

        rpaagrp = AccessGroup.objects.filter(
            agrp_name="Some other access group"
        ).prefetch_related("cpd")
        rpaagrp_cpd = CategoryOfPersonalData.objects.filter(accessgroups__in=rpaagrp)
        expected_agrp_cpd = "1 3"
        actual_agrp_cpd = (
            str(rpaagrp_cpd[0].cpd_index) + " " + str(rpaagrp_cpd[1].cpd_index)
        )
        assert actual_agrp_cpd == expected_agrp_cpd
        detail_view = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/", user="kuno"
        )
        soup = detail_view.html
        agrp_data = soup.find(id="info-agrp").get_text()
        assert ("Access group designation" in agrp_data) is True
        assert ("Data access rights" in agrp_data) is True
        assert ("Applies to data categories:" in agrp_data) is True


class RPACreateTranViewTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete.json",
    ]

    def test_update_tran(self):
        """Test whether a Transparency model instance can be
        successfully updated.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/tran/", user="kuno"
        )
        form = editpage.forms["edit-tran"]
        form["tran_choices"] = ["tran_online", "tran_other"]
        form["tran_explanation"] = "Some explanation"
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert Transparency.objects.exists() is True
        rpatran = Transparency.objects.filter().first()
        assert rpatran.tran_explanation == "Some explanation"

    def test_update_tran_with_empty_tran_descr(self):
        """Test whether a Transparency model instance update will fail
        with empty tran_explanation.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/tran/", user="kuno"
        )
        form = editpage.forms["edit-tran"]
        form["tran_choices"] = []
        form["tran_explanation"] = ""
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("You must choose at least one way to inform" in res) is True


class RPACreateDproViewTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete.json",
    ]

    def test_update_dpro(self):
        """Test whether a DataProcessor model instance can be
        successfully updated.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/dpro/", user="kuno"
        )
        form = editpage.forms["edit-dpro"]
        form["dpro_is_assigned"] = "true"
        form["dpro_name"] = "Some data processor"
        form["dpro_contact"] = "Some contact person at some data processor"
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert DataProcessor.objects.exists() is True
        rpadpro = DataProcessor.objects.filter().first()
        assert rpadpro.dpro_name == "Some data processor"
        detail_view = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/", user="kuno"
        )
        assert ("Data processor - Name" in detail_view) is True
        assert ("Data processor - Contact person" in detail_view) is True

    def test_update_dpro_with_empty_dpro_name(self):
        """Test whether a DataProcessor model instance update will fail
        with empty dpro_name.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/dpro/", user="kuno"
        )
        form = editpage.forms["edit-dpro"]
        form["dpro_is_assigned"] = "unknown"
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("Is there a data processor? Choose either" in res) is True
        form["dpro_is_assigned"] = "true"
        form["dpro_name"] = ""
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert (
            "If there is a data processor, please enter their contact data" in res
        ) is True


class RPACreatePiaViewTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete.json",
    ]

    def test_update_pia(self):
        """Test whether a PrivacyImpactAssessment model instance can be
        successfully updated.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/pia/", user="kuno"
        )
        form = editpage.forms["edit-pia"]
        form["pia_required"] = "true"
        form["pia_results"] = [
            "pia_additional_measures",
        ]
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert PrivacyImpactAssessment.objects.exists() is True
        rpapia = PrivacyImpactAssessment.objects.filter().first()
        assert rpapia.pia_results == [
            "pia_additional_measures",
        ]
        detail_view = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/", user="kuno"
        )
        assert ("PIA required" in detail_view) is True
        assert ("PIA results" in detail_view) is True

    def test_update_pia_with_empty_pia_name(self):
        """Test whether a PrivacyImpactAssessment model instance update
        will fail with empty pia_results.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/pia/", user="kuno"
        )
        form = editpage.forms["edit-pia"]
        form["pia_required"] = "unknown"
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("Is a privacy impact assessment required" in res) is True
        form["pia_required"] = "false"
        form["pia_not_required_reason"] = [
            "pia_nr_special_categories",
            "pia_nr_monitoring_public",
            "pia_nr_required_list",
        ]
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert (
            "Read and check all circumstances that must not be present" in res
        ) is True
        form["pia_required"] = "true"
        form["pia_results"] = []
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("A PIA must have one single result" in res) is True


class RPACreateTomViewTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete.json",
    ]

    def test_update_tom(self):
        """Test whether a TOM model instance can be successfully
        updated.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/tom/", user="kuno"
        )
        form = editpage.forms["edit-tom"]
        form["tom_handling"] = "tom_in_rpa"
        form["tom_pseudonym_selection"] = []
        form["tom_pseudonym"] = "Some measures regarding pseudonymization"
        form["tom_encryption_selection"] = []
        form["tom_encryption"] = "Some measures regarding encryption"
        form["tom_integrity_selection"] = []
        form["tom_integrity"] = "Some measures regarding integrity/confidentiality"
        form["tom_availability_selection"] = []
        form["tom_availability"] = "Some measures regarding availability/resilience"
        form["tom_evaluation_selection"] = []
        form["tom_evaluation"] = "Some measures regarding evaluation"
        form["tom_appropriation_selection"] = []
        form["tom_appropriation"] = "Some measures regarding appropriation"
        form["tom_transparency_selection"] = []
        form["tom_transparency"] = "Some measures regarding transparency"
        form["tom_subject_rights_selection"] = []
        form["tom_subject_rights"] = "Some measures regarding subject rights"
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert TOM.objects.exists() is True
        rpatom = TOM.objects.filter().first()
        assert (
            rpatom.tom_integrity == "Some measures regarding integrity/confidentiality"
        )
        detail_view = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/", user="kuno"
        )
        assert ("TOM: Pseudonymization" in detail_view) is True
        assert ("TOM: Encryption" in detail_view) is True
        assert ("TOM: Integrity and confidentiality" in detail_view) is True
        assert ("TOM: Availability and Resilience" in detail_view) is True
        assert ("TOM: Evaluation" in detail_view) is True
        assert ("TOM: Appropriation" in detail_view) is True
        assert ("TOM: Transparency" in detail_view) is True
        assert ("TOM: Subject rights" in detail_view) is True
        assert ("Other or additional measures" in detail_view) is True
        form = editpage.forms["edit-tom"]
        form["tom_handling"] = "tom_in_rpa"
        form["tom_pseudonym_selection"] = [
            "tom_pseudo_no_pseudo",
        ]
        form["tom_pseudonym"] = "Some measures regarding pseudonymization"
        form["tom_encryption_selection"] = [
            "tom_enc_public_net",
        ]
        form["tom_encryption"] = "Some measures regarding encryption"
        form["tom_integrity_selection"] = [
            "tom_int_password",
        ]
        form["tom_integrity"] = "Some measures regarding integrity/confidentiality"
        form["tom_availability_selection"] = [
            "tom_avail_no_conseq",
        ]
        form["tom_availability"] = "Some measures regarding availability/resilience"
        form["tom_evaluation_selection"] = [
            "tom_eval_guidelines_self",
        ]
        form["tom_evaluation"] = "Some measures regarding evaluation"
        form["tom_appropriation_selection"] = [
            "tom_appro_awareness",
        ]
        form["tom_appropriation"] = "Some measures regarding appropriation"
        form["tom_transparency_selection"] = [
            "tom_tran_proc",
        ]
        form["tom_transparency"] = "Some measures regarding transparency"
        form["tom_subject_rights_selection"] = [
            "tom_srights_known",
        ]
        form["tom_subject_rights"] = "Some measures regarding subject rights"
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert TOM.objects.exists() is True
        rpatom = TOM.objects.filter().first()
        assert rpatom.tom_pseudonym_selection == [
            "tom_pseudo_no_pseudo",
        ]
        assert rpatom.tom_encryption_selection == [
            "tom_enc_public_net",
        ]
        assert rpatom.tom_integrity_selection == [
            "tom_int_password",
        ]
        assert rpatom.tom_availability_selection == [
            "tom_avail_no_conseq",
        ]
        assert rpatom.tom_evaluation_selection == [
            "tom_eval_guidelines_self",
        ]
        assert rpatom.tom_appropriation_selection == [
            "tom_appro_awareness",
        ]
        assert rpatom.tom_transparency_selection == [
            "tom_tran_proc",
        ]
        assert rpatom.tom_subject_rights_selection == [
            "tom_srights_known",
        ]
        detail_view = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/", user="kuno"
        )


class RPACreateAnnexViewTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete.json",
    ]

    def test_update_annex(self):
        """Test whether a RPAAnnex model instance can be successfully
        updated.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/annex/", user="kuno"
        )
        form = editpage.forms["edit-annex"]
        form["form-0-annex_index"] = 1
        form["form-0-annex_name"] = "Some annex"
        form["form-1-annex_index"] = 2
        form["form-1-annex_name"] = "Some different annex"
        form["form-2-annex_index"] = 3
        form["form-2-annex_name"] = "Some even more different annex"
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert RPAAnnex.objects.exists() is True
        rpaannex = RPAAnnex.objects.filter(annex_index=3).get()
        assert rpaannex.annex_name == "Some even more different annex"

    def test_update_annex_with_index_already_in_use(self):
        """Test whether a RPAAnnex model instance update will fail with
        annex_index already in use.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/annex/", user="kuno"
        )
        form = editpage.forms["edit-annex"]
        form["form-0-annex_index"] = 1
        form["form-0-annex_name"] = "Some other annex"
        form["form-1-annex_index"] = 1
        form["form-1-annex_name"] = "Some important annex"
        form["form-2-annex_index"] = 3
        form["form-2-annex_name"] = "Some even more important annex"
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("Index already in use" in res) is True

    def test_update_annex_with_empty_annex_name(self):
        """Test whether a RPAAnnex model instance update will fail with
        empty annex_name.
        """
        completerpa = Rpa.objects.get(pk="1")
        editpage = self.app.get(
            "/rpa/myrpas/detail/" + completerpa.slug + "/edit/annex/", user="kuno"
        )
        form = editpage.forms["edit-annex"]
        form["form-0-annex_index"] = 1
        form["form-0-annex_name"] = "Some other annex"
        form["form-1-annex_index"] = 2
        form["form-1-annex_name"] = "Some important annex"
        form["form-2-annex_index"] = 3
        form["form-2-annex_name"] = ""
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("Annex entry missing" in res) is True

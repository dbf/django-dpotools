from django_webtest import WebTest

from breach.models import (
    Breach,
    BreachTimeLine,
    BreachDescription,
    BreachAffectedData,
    BreachAffectedSubjects,
    BreachConsequences,
    BreachMeasures,
    BreachCommunication,
    BreachAnnex,
)


class BreachDeleteViewTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-empty-kuno.json",
    ]

    def test_delete_confirm_cancel_mybreaches(self):
        """Test whether users can delete their own breaches from
        mybreaches list and whether cancelling the deletion confirmation
        works.
        """
        ownbreach = Breach.objects.get(pk="1")
        deletepage = self.app.get(
            "/breach/mybreaches/detail/" + ownbreach.slug + "/delete/", user="kuno"
        )
        form = deletepage.forms["delete-confirmation"]
        res = form.submit("cancel", value="Cancel")
        assert deletepage.status_int == 200
        assert Breach.objects.exists() is True
        res = form.submit(value="Confirm")
        assert res.status_int == 302
        assert Breach.objects.exists() is False


class AllBreachDeleteViewTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-empty-kuno.json",
    ]

    def test_delete_confirm_cancel_allbreaches(self):
        """Test whether dpo user can delete breaches from allbreaches
        list and whether cancelling the deletion confirmation works.
        """
        otherbreach = Breach.objects.get(pk="1")
        deletepage = self.app.get(
            "/breach/allbreaches/detail/" + otherbreach.slug + "/delete/", user="hugo"
        )
        form = deletepage.forms["delete-confirmation"]
        res = form.submit("cancel", value="Cancel")
        assert deletepage.status_int == 200
        assert Breach.objects.exists() is True
        res = form.submit(value="Confirm")
        assert res.status_int == 302
        assert Breach.objects.exists() is False


class BreachTimeLineTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-complete.json",
    ]

    def test_btl_template_details(self):
        """Test BreachTimeLine to please coverage for commontemplate."""
        completebreach = Breach.objects.get(pk="1")
        editpage = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/edit/btl/",
            user="kuno",
        )
        # 1st form run
        form = editpage.forms["edit-btl"]
        form["btl_start"] = "2022-12-07"
        form["btl_start_known"] = "yes"
        form["btl_end"] = "2022-12-08"
        form["btl_ongoing"] = "no"
        form["btl_may_recur"] = "no"
        form["btl_noticed"] = "2022-12-08"
        form["btl_notif_delay_reason"] = (
            "Some circumlocution for inadequate organisation"
        )
        form["btl_other_supauth"] = "Some other competent supervisory authority"
        form["btl_supauth_od"] = "Some organisational descriptor"
        form["btl_remarks"] = "Some remarks"
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert BreachTimeLine.objects.exists() is True
        detail_view = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/", user="kuno"
        )
        soup = detail_view.html
        btl_data = soup.find(id="info-btl").get_text()
        assert ("Some other competent supervisory authority" in btl_data) is True
        assert ("Is there likely to be a repeat of the breach?\nNo" in btl_data) is True
        # 2nd form run
        form = editpage.forms["edit-btl"]
        form["btl_start"] = None
        form["btl_start_known"] = "no"
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert BreachTimeLine.objects.exists() is True
        detail_view = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/", user="kuno"
        )
        soup = detail_view.html
        btl_data = soup.find(id="info-btl").get_text()
        assert ("Start of the breach\nUnknown" in btl_data) is True


class BreachDescriptionTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-complete.json",
    ]

    def test_bdesc_template_details(self):
        """Test BreachDescription to please coverage for commontemplate."""
        completebreach = Breach.objects.get(pk="1")
        editpage = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/edit/bdesc/",
            user="kuno",
        )
        form = editpage.forms["edit-bdesc"]
        form["bdesc_selection"] = []
        form["bdesc_selection_other"] = "Some other boo-boo"
        form["bdesc_description"] = "Some boo-boo description"
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert BreachDescription.objects.exists() is True
        detail_view = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/", user="kuno"
        )
        soup = detail_view.html
        bdesc_data = soup.find(id="info-bdesc").get_text()
        assert ("Type of breach" in bdesc_data) is True
        assert ("Additional or other types of breaches" in bdesc_data) is True
        assert ("Breach description" in bdesc_data) is True


class BreachAffectedDataTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-complete.json",
    ]

    def test_baffd_template_details(self):
        """Test BreachAffectedData to please coverage for
        commontemplate.
        """
        completebreach = Breach.objects.get(pk="1")
        editpage = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/edit/baffd/",
            user="kuno",
        )
        # 1st form run
        form = editpage.forms["edit-baffd"]
        form["baffd_selection"] = []
        form["baffd_selection_other"] = "Some other data"
        form["baffd_special_selection"] = [
            "special_not_known_yet",
        ]
        form["baffd_special_unknown_reason"] = (
            "Some circumlocution for inadequate organisation"
        )
        form["baffd_data_min"] = "1"
        form["baffd_data_max"] = "2"
        form["baffd_remarks"] = "Some remarks"
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert BreachAffectedData.objects.exists() is True
        detail_view = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/", user="kuno"
        )
        soup = detail_view.html
        baffd_data = soup.find(id="info-baffd").get_text()
        assert ("Affected data" in baffd_data) is True
        assert ("Affected data (additional or other)" in baffd_data) is True
        assert ("Affected data (special categories)" in baffd_data) is True
        assert (
            "Reason for special data categories being unknown" in baffd_data
        ) is True
        assert ("Estimated minimum of affected data sets" in baffd_data) is True
        assert ("Estimated maximum of affected data sets" in baffd_data) is True
        # 2nd form run
        form = editpage.forms["edit-baffd"]
        form["baffd_selection"] = [
            "not_known_yet",
        ]
        form["baffd_special_selection"] = [
            "trade_union_membership",
        ]
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert BreachAffectedData.objects.exists() is True
        detail_view = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/", user="kuno"
        )
        soup = detail_view.html
        baffd_data = soup.find(id="info-baffd").get_text()
        assert ("Affected data\nNot known (yet)" in baffd_data) is True


class BreachAffectedSubjectsTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-complete.json",
    ]

    def test_baffs_template_details(self):
        """Test BreachAffectedSubjects to please coverage for
        commontemplate.
        """
        completebreach = Breach.objects.get(pk="1")
        editpage = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/edit/baffs/",
            user="kuno",
        )
        # 1st form run
        form = editpage.forms["edit-baffs"]
        form["baffs_selection"] = [
            "own_employees",
        ]
        form["baffs_selection_other"] = "Some other affected group of persons"
        form["baffs_datasubjects_min"] = "1"
        form["baffs_datasubjects_max"] = "2"
        form["baffs_remarks"] = "Some remarks"
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert BreachAffectedSubjects.objects.exists() is True
        detail_view = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/", user="kuno"
        )
        soup = detail_view.html
        baffs_data = soup.find(id="info-baffs").get_text()
        assert (
            "Data subject categories (groups of persons) affected by the breach"
            in baffs_data
        ) is True
        assert (
            "Other or additional data subject categories affected by the breach"
            in baffs_data
        ) is True
        assert ("Estimated minimum number of data subjects" in baffs_data) is True
        assert ("Estimated maximum number of data subjects" in baffs_data) is True
        assert ("Remarks on affected data subject categories" in baffs_data) is True
        # 2nd form run
        form = editpage.forms["edit-baffs"]
        form["baffs_selection"] = [
            "not_known_yet",
        ]
        form["baffs_selection_other"] = ""
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert BreachAffectedSubjects.objects.exists() is True
        detail_view = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/", user="kuno"
        )
        soup = detail_view.html
        baffs_data = soup.find(id="info-baffs").get_text()
        assert (
            "Data subject categories (groups of persons) affected by the breach\nNot known (yet)"
            in baffs_data
        ) is True
        # 3rd form run
        form = editpage.forms["edit-baffs"]
        form["baffs_selection"] = []
        form["baffs_selection_other"] = "Some other affected group of persons"
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert BreachAffectedSubjects.objects.exists() is True
        detail_view = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/", user="kuno"
        )
        soup = detail_view.html
        baffs_data = soup.find(id="info-baffs").get_text()
        assert ("Other data subject categories, cf. below." in baffs_data) is True


class BreachConsequencesTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-complete.json",
    ]

    def test_bcons_template_details(self):
        """Test BreachConsequences to please coverage for
        commontemplate.
        """
        completebreach = Breach.objects.get(pk="1")
        editpage = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/edit/bcons/",
            user="kuno",
        )
        form = editpage.forms["edit-bcons"]
        form["bcons_confidentiality_selection"] = [
            "dissemination_to_3rd_party",
        ]
        form["bcons_confidentiality"] = "Some other consequences re conf"
        form["bcons_integrity_selection"] = [
            "data_falsified",
        ]
        form["bcons_integrity"] = "Some other consequences re int"
        form["bcons_availability_selection"] = [
            "data_unavailable",
        ]
        form["bcons_availability"] = "Some other consequences re avail"
        form["bcons_consequences_descr"] = "Some description of consequences"
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert BreachConsequences.objects.exists() is True
        detail_view = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/", user="kuno"
        )
        soup = detail_view.html
        bcons_data = soup.find(id="info-bcons").get_text()
        assert ("Breaches of confidentiality" in bcons_data) is True
        assert ("Breaches of integrity" in bcons_data) is True
        assert ("Breaches of availability" in bcons_data) is True
        assert (
            "Description of likely consequences for the data subjects" in bcons_data
        ) is True


class BreachMeasuresTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-complete.json",
    ]

    def test_bmeasures_template_details(self):
        """Test BreachMeasures to please coverage for commontemplate."""
        completebreach = Breach.objects.get(pk="1")
        editpage = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/edit/bmeasures/",
            user="kuno",
        )
        # 1st form run
        form = editpage.forms["edit-bmeasures"]
        form["bmeasures_taken"] = "Some measures taken"
        form["bmeasures_proposed"] = "Some measures proposed"
        form["bmeasures_no_measures_reason"] = ""
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert BreachMeasures.objects.exists() is True
        detail_view = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/", user="kuno"
        )
        soup = detail_view.html
        bmeasures_data = soup.find(id="info-bmeasures").get_text()
        assert ("Measures already taken" in bmeasures_data) is True
        assert ("Measures proposed" in bmeasures_data) is True
        # 2nd form run
        form = editpage.forms["edit-bmeasures"]
        form["bmeasures_taken"] = ""
        form["bmeasures_proposed"] = ""
        form["bmeasures_no_measures_reason"] = "Some helpless babble"
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert BreachMeasures.objects.exists() is True
        detail_view = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/", user="kuno"
        )
        soup = detail_view.html
        bmeasures_data = soup.find(id="info-bmeasures").get_text()
        assert (
            "Reason for no measures\nSome helpless babble" in bmeasures_data
        ) is True


class BreachCommunicationTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-complete.json",
    ]

    def test_bcomm_template_details(self):
        """Test BreachCommunication to please coverage for commontemplate."""
        completebreach = Breach.objects.get(pk="1")
        editpage = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/edit/bcomm/",
            user="kuno",
        )
        # 1st form run
        form = editpage.forms["edit-bcomm"]
        form["bcomm_communication_selection"] = "already_happened"
        form["bcomm_no_communication_reason"] = ""
        form["bcomm_modality_selection"] = [
            "personal_dialogue",
        ]
        form["bcomm_modality"] = ""
        form["bcomm_number_of_data_subjects"] = "1679"
        form["bcomm_remarks"] = "Some remarks on communication"
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert BreachCommunication.objects.exists() is True
        detail_view = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/", user="kuno"
        )
        soup = detail_view.html
        bcomm_data = soup.find(id="info-bcomm").get_text()
        assert (
            "Communication\nAlready done (date and details below)." in bcomm_data
        ) is True
        assert ("Modality of communication" in bcomm_data) is True
        assert ("Number of persons already informed" in bcomm_data) is True
        assert ("Remarks on communication" in bcomm_data) is True
        # 2nd form run
        form = editpage.forms["edit-bcomm"]
        form["bcomm_communication_selection"] = "will_not_happen"
        form["bcomm_no_communication_reason"] = "Some embarrassing excuses"
        form["bcomm_modality_selection"] = []
        form["bcomm_modality"] = ""
        form["bcomm_number_of_data_subjects"] = ""
        form["bcomm_remarks"] = ""
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert BreachCommunication.objects.exists() is True
        detail_view = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/", user="kuno"
        )
        soup = detail_view.html
        bcomm_data = soup.find(id="info-bcomm").get_text()
        assert (
            "Communication\nIs not being considered (reason below)." in bcomm_data
        ) is True
        assert ("Reason for no communication" in bcomm_data) is True
        # 3rd form run
        form = editpage.forms["edit-bcomm"]
        form["bcomm_communication_selection"] = "already_happened"
        form["bcomm_no_communication_reason"] = ""
        form["bcomm_modality_selection"] = []
        form["bcomm_modality"] = "Mounted messenger"
        form["bcomm_number_of_data_subjects"] = "1679"
        form["bcomm_remarks"] = "Some remarks on communication"
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert BreachCommunication.objects.exists() is True
        detail_view = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/", user="kuno"
        )
        soup = detail_view.html
        bcomm_data = soup.find(id="info-bcomm").get_text()
        assert (
            "Modality of communication (other or additional)\nMounted messenger"
            in bcomm_data
        ) is True


class BreachCreateAnnexViewTest(WebTest):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-complete.json",
    ]

    def test_update_bannex(self):
        """Test whether a BreachAnnex model instance can be successfully
        updated.
        """
        completebreach = Breach.objects.get(pk="1")
        editpage = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/edit/bannex/",
            user="kuno",
        )
        form = editpage.forms["edit-bannex"]
        form["form-0-bannex_index"] = 1
        form["form-0-bannex_name"] = "Some annex"
        form["form-1-bannex_index"] = 2
        form["form-1-bannex_name"] = "Some different annex"
        form["form-2-bannex_index"] = 3
        form["form-2-bannex_name"] = "Some even more different annex"
        res = form.submit(value="Submit")
        assert res.status_int == 302
        assert BreachAnnex.objects.exists() is True
        breachannex = BreachAnnex.objects.filter(bannex_index=3).get()
        assert breachannex.bannex_name == "Some even more different annex"

    def test_update_bannex_with_index_already_in_use(self):
        """Test whether a BreachAnnex model instance update will fail with
        bannex_index already in use.
        """
        completebreach = Breach.objects.get(pk="1")
        editpage = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/edit/bannex/",
            user="kuno",
        )
        form = editpage.forms["edit-bannex"]
        form["form-0-bannex_index"] = 1
        form["form-0-bannex_name"] = "Some other annex"
        form["form-1-bannex_index"] = 1
        form["form-1-bannex_name"] = "Some important annex"
        form["form-2-bannex_index"] = 3
        form["form-2-bannex_name"] = "Some even more important annex"
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("Index already in use" in res) is True

    def test_update_annex_with_empty_bannex_name(self):
        """Test whether a BreachAnnex model instance update will fail with
        empty bannex_name.
        """
        completebreach = Breach.objects.get(pk="1")
        editpage = self.app.get(
            "/breach/mybreaches/detail/" + completebreach.slug + "/edit/bannex/",
            user="kuno",
        )
        form = editpage.forms["edit-bannex"]
        form["form-0-bannex_index"] = 1
        form["form-0-bannex_name"] = "Some other annex"
        form["form-1-bannex_index"] = 2
        form["form-1-bannex_name"] = "Some important annex"
        form["form-2-bannex_index"] = 3
        form["form-2-bannex_name"] = ""
        res = form.submit(value="Submit")
        assert res.status_int == 200
        assert ("Annex entry missing" in res) is True

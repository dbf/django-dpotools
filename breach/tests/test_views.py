import datetime
from io import BytesIO

from django.test import TestCase
from django.test import Client
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from PyPDF2 import PdfReader

from breach.views import (
    BreachHintsView,
    MyBreachesView,
    AllBreachesView,
    BreachDetailView,
    BreachDetailPDFView,
    BreachDeleteView,
    AllBreachDeleteView,
    BreachEditView,
    BreachCreateView,
    BreachCreateDconView,
    BreachCreateBtlView,
    BreachCreateBdescView,
    BreachCreateBaffdView,
    BreachCreateBaffsView,
    BreachCreateBconsView,
    BreachCreateBmeasuresView,
    BreachCreateBcommView,
)

from breach.models import (
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


class BreachHintsViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
    ]

    def setUp(self):
        self.client = Client()

    def test_breach_hints_template(self):
        """Test whether hints are correctly presented to logged in user."""
        self.client.login(username="kuno", password="kuno")
        response = self.client.get(reverse("breach:breach_hints"))
        self.assertTemplateUsed(response, "breach/breach_hints.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, BreachHintsView)


class MyBreachesViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-empty-kuno.json",
    ]

    def setUp(self):
        self.client = Client()
        self.emptybreach = Breach.objects.get(pk="1")

    def test_breach_mybreaches_visible_to_superuser(self):
        testuser = User.objects.get(pk="1")
        self.client.force_login(testuser)
        self.assertTrue(testuser.is_superuser)
        response = self.client.get(reverse("breach:my_breaches"))
        self.assertTemplateUsed(response, "breach/breach_view.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, MyBreachesView)

    def test_breach_mybreaches_visible_to_dpo(self):
        testuser = User.objects.get(pk="3")
        self.client.force_login(testuser)
        self.assertTrue(testuser.is_staff)
        self.assertTrue(testuser.groups.filter(name="dpo").exists())
        response = self.client.get(reverse("breach:my_breaches"))
        self.assertTemplateUsed(response, "breach/breach_view.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, MyBreachesView)

    def test_breach_mybreaches_visible_to_user(self):
        testuser = User.objects.get(pk="2")
        self.client.force_login(testuser)
        self.assertFalse(testuser.is_superuser)
        self.assertFalse(testuser.is_staff)
        response = self.client.get(reverse("breach:my_breaches"))
        self.assertTemplateUsed(response, "breach/breach_view.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, MyBreachesView)

    def test_breach_mybreaches_no_breach_reports(self):
        testuser = User.objects.get(pk="2")
        self.client.force_login(testuser)
        self.assertFalse(testuser.is_superuser)
        self.assertFalse(testuser.is_staff)
        self.emptybreach.delete()
        response = self.client.get(reverse("breach:my_breaches"))
        self.assertTemplateUsed(response, "breach/breach_view.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, MyBreachesView)
        self.assertContains(response, "No breach reports available.")

    def test_rpa_myrpas_user_without_breach_reports_and_full_name(self):
        testuser_without_fn = User.objects.create_user(
            username="ottokar", password="ottokar"
        )
        self.client.force_login(testuser_without_fn)
        self.assertFalse(testuser_without_fn.is_superuser)
        self.assertFalse(testuser_without_fn.is_staff)
        response = self.client.get(reverse("breach:my_breaches"))
        self.assertTemplateUsed(response, "breach/breach_view.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, MyBreachesView)
        self.assertContains(response, "No breach reports available.")


class AllBreachesViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-empty-kuno.json",
    ]

    def setUp(self):
        self.client = Client()
        self.emptybreach = Breach.objects.get(pk="1")

    def test_breach_allbreaches_visible_to_superuser(self):
        testuser = User.objects.get(pk="1")
        self.client.force_login(testuser)
        self.assertTrue(testuser.is_superuser)
        response = self.client.get(reverse("breach:all_breaches"))
        self.assertTemplateUsed(response, "breach/breach_view_all.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, AllBreachesView)

    def test_breach_allbreaches_visible_to_dpo(self):
        testuser = User.objects.get(pk="3")
        self.client.force_login(testuser)
        self.assertTrue(testuser.is_staff)
        self.assertTrue(testuser.groups.filter(name="dpo").exists())
        response = self.client.get(reverse("breach:all_breaches"))
        self.assertTemplateUsed(response, "breach/breach_view_all.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, AllBreachesView)

    def test_breach_allbreaches_denied_to_user(self):
        testuser = User.objects.get(pk="2")
        self.client.force_login(testuser)
        self.assertFalse(testuser.is_superuser)
        self.assertFalse(testuser.is_staff)
        response = self.client.get(reverse("breach:all_breaches"))
        self.assertEqual(response.status_code, 403)

    def test_breach_allbreaches_no_breach_reports(self):
        testuser = User.objects.get(pk="3")
        self.client.force_login(testuser)
        self.assertTrue(testuser.is_staff)
        self.emptybreach.delete()
        response = self.client.get(reverse("breach:all_breaches"))
        self.assertTemplateUsed(response, "breach/breach_view_all.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, AllBreachesView)
        self.assertContains(response, "No breach reports available.")


class BreachDetailViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-complete.json",
        "testbreach-empty-hugo.json",
    ]

    def setUp(self):
        self.client = Client()

    def test_breach_detail_user_own(self):
        """Test whether non-privileged users can detail view their own
        breaches.
        """
        testuser = User.objects.get(pk="2")
        self.client.force_login(testuser)
        ownbreach = Breach.objects.get(pk="1")
        reference = (
            ownbreach.slug
            + "-"
            + datetime.date.strftime(ownbreach.report_date, "%Y%m%d")
        )
        response = self.client.get("/breach/mybreaches/detail/" + ownbreach.slug + "/")
        self.assertTemplateUsed(response, "breach/breach_htmltemplate.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reference)
        self.assertIs(response.resolver_match.func.view_class, BreachDetailView)

    def test_breach_detail_user_other(self):
        """Test whether non-privileged users can detail view breaches
        of other users. Should result in 403.
        """
        testuser = User.objects.get(pk="2")
        self.client.force_login(testuser)
        otherbreach = Breach.objects.get(pk="2")
        response = self.client.get(
            "/breach/mybreaches/detail/" + otherbreach.slug + "/"
        )
        self.assertEqual(response.status_code, 403)

    def test_breach_detail_su_other(self):
        """Test whether superusers can detail view breaches of other users."""
        testuser = User.objects.get(pk="1")
        self.client.force_login(testuser)
        otherbreach = Breach.objects.get(pk="1")
        reference = (
            otherbreach.slug
            + "-"
            + datetime.date.strftime(otherbreach.report_date, "%Y%m%d")
        )
        response = self.client.get(
            "/breach/mybreaches/detail/" + otherbreach.slug + "/"
        )
        self.assertTemplateUsed(response, "breach/breach_htmltemplate.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reference)
        self.assertIs(response.resolver_match.func.view_class, BreachDetailView)

    def test_breach_detail_dpo_other(self):
        """Test whether dpo users can detail view breaches of other users."""
        testuser = User.objects.get(pk="3")
        self.client.force_login(testuser)
        otherbreach = Breach.objects.get(pk="1")
        reference = (
            otherbreach.slug
            + "-"
            + datetime.date.strftime(otherbreach.report_date, "%Y%m%d")
        )
        response = self.client.get(
            "/breach/mybreaches/detail/" + otherbreach.slug + "/"
        )
        self.assertTemplateUsed(response, "breach/breach_htmltemplate.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reference)


class BreachDetailPDFViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-empty-kuno.json",
        "testbreach-empty-hugo.json",
    ]

    def setUp(self):
        self.client = Client()

    def test_breach_detail_pdf_user_own(self):
        """Test whether non-privileged users can detail view their own
        breaches (PDF export).
        """
        testuser = User.objects.get(pk="2")
        self.client.force_login(testuser)
        ownbreach = Breach.objects.get(pk="1")
        reference = (
            ownbreach.slug
            + "-"
            + datetime.date.strftime(ownbreach.report_date, "%Y%m%d")
        )
        response = self.client.get(
            "/breach/mybreaches/detail/" + ownbreach.slug + "/pdf/"
        )
        file = BytesIO()
        file.write(response.content)
        file.seek(0)
        reader = PdfReader(file)
        # reference string should be on 1st page of pdf
        page = reader.pages[0]
        text = page.extract_text()
        self.assertTemplateUsed(response, "breach/breach_pdftemplate.html")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(reference in text)
        self.assertIs(response.resolver_match.func.view_class, BreachDetailPDFView)

    def test_breach_detail_pdf_filename(self):
        """Test whether filename for PDF export will be set correctly."""
        testuser = User.objects.get(pk="2")
        self.client.force_login(testuser)
        ownbreach = Breach.objects.get(pk="1")
        response = self.client.get(
            "/breach/mybreaches/detail/" + ownbreach.slug + "/pdf/"
        )
        con_dis = response["Content-Disposition"]
        expectedfn = (
            "Breach-"
            + ownbreach.slug
            + "-"
            + str(datetime.date.today().strftime("%Y%m%d"))
            + ".pdf"
        )
        self.assertTrue(expectedfn in con_dis)

    def test_breach_detail_pdf_user_other(self):
        """Test whether non-privileged users can detail view breaches
        of other users (pdf export). Should result in 403.
        """
        testuser = User.objects.get(pk="2")
        self.client.force_login(testuser)
        otherbreach = Breach.objects.get(pk="2")
        response = self.client.get(
            "/breach/mybreaches/detail/" + otherbreach.slug + "/pdf/"
        )
        self.assertEqual(response.status_code, 403)


class BreachDeleteViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-empty-kuno.json",
    ]

    def setUp(self):
        self.client = Client()
        self.emptybreach = Breach.objects.get(pk="1")

    def test_breach_delete_visible_to_user(self):
        testuser = User.objects.get(pk="2")
        self.client.force_login(testuser)
        self.assertFalse(testuser.is_superuser)
        self.assertFalse(testuser.is_staff)
        response = self.client.get(
            "/breach/mybreaches/detail/" + self.emptybreach.slug + "/delete/"
        )
        self.assertTemplateUsed(response, "breach/breach_delete_confirmation.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, BreachDeleteView)


class AllBreachDeleteViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-empty-kuno.json",
    ]

    def setUp(self):
        self.client = Client()
        self.emptybreach = Breach.objects.get(pk="1")

    def test_breach_allbreaches_delete_visible_to_superuser(self):
        testuser = User.objects.get(pk="1")
        self.client.force_login(testuser)
        self.assertTrue(testuser.is_superuser)
        response = self.client.get(
            "/breach/allbreaches/detail/" + self.emptybreach.slug + "/delete/"
        )
        self.assertTemplateUsed(response, "breach/breach_delete_confirmation.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, AllBreachDeleteView)

    def test_breach_allbreaches_delete_visible_to_dpo(self):
        testuser = User.objects.get(pk="3")
        self.client.force_login(testuser)
        self.assertTrue(testuser.is_staff)
        response = self.client.get(
            "/breach/allbreaches/detail/" + self.emptybreach.slug + "/delete/"
        )
        self.assertTemplateUsed(response, "breach/breach_delete_confirmation.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, AllBreachDeleteView)

    def test_breach_allbreaches_delete_denied_to_user(self):
        testuser = User.objects.get(pk="2")
        self.client.force_login(testuser)
        self.assertFalse(testuser.is_superuser)
        self.assertFalse(testuser.is_staff)
        response = self.client.get(
            "/breach/allbreaches/detail/" + self.emptybreach.slug + "/delete/"
        )
        self.assertEqual(response.status_code, 403)


class BreachEditViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-empty-kuno.json",
    ]

    def setUp(self):
        self.client = Client()
        self.emptybreach = Breach.objects.get(pk="1")

    def test_breach_edit_visible_to_superuser(self):
        testuser = User.objects.get(pk="1")
        self.client.force_login(testuser)
        self.assertTrue(testuser.is_superuser)
        response = self.client.get(
            "/breach/allbreaches/detail/" + self.emptybreach.slug + "/edit/"
        )
        self.assertTemplateUsed(response, "breach/breach_edit.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, BreachEditView)

    def test_breach_edit_visible_to_dpo(self):
        testuser = User.objects.get(pk="3")
        self.client.force_login(testuser)
        self.assertTrue(testuser.is_staff)
        self.assertTrue(testuser.groups.filter(name="dpo").exists())
        response = self.client.get(
            "/breach/allbreaches/detail/" + self.emptybreach.slug + "/edit/"
        )
        self.assertTemplateUsed(response, "breach/breach_edit.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, BreachEditView)

    def test_breach_edit_visible_to_user(self):
        testuser = User.objects.get(pk="2")
        self.client.force_login(testuser)
        self.assertFalse(testuser.is_superuser)
        self.assertFalse(testuser.is_staff)
        response = self.client.get(
            "/breach/mybreaches/detail/" + self.emptybreach.slug + "/edit/"
        )
        self.assertTemplateUsed(response, "breach/breach_edit.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, BreachEditView)


class BreachCreateViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
    ]

    def setUp(self):
        self.client = Client()

    def test_createview_template(self):
        """Test whether BreachCreateView is correctly presented to
        logged in user.
        """
        self.client.login(username="kuno", password="kuno")
        response = self.client.get(reverse("breach:breach_create"))
        self.assertTemplateUsed(response, "breach/breach_create_slug.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, BreachCreateView)

    def test_createview_create(self):
        testuser = User.objects.get(pk="2")
        form_data = {
            "user": 2,
            "slug": "testbreach",
            "breach_bumper": True,
            "helptext_display_default": "show",
        }
        self.client.force_login(testuser)
        response = self.client.post(reverse("breach:breach_create"), data=form_data)
        self.assertEqual(302, response.status_code)
        self.assertTrue(Breach.objects.exists())


class BreachCreateDconViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-empty-kuno.json",
    ]

    def setUp(self):
        self.client = Client()
        self.emptybreach = Breach.objects.get(pk="1")

    def test_createdconview_template(self):
        self.client.login(username="kuno", password="kuno")
        response = self.client.get(
            "/breach/mybreaches/detail/" + self.emptybreach.slug + "/edit/dcon/"
        )
        self.assertTemplateUsed(response, "breach/breach_create_dcon.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, BreachCreateDconView)

    def test_createdconview_create(self):
        testuser = User.objects.get(pk="2")
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
        self.client.force_login(testuser)
        response = self.client.post(
            "/breach/mybreaches/detail/" + self.emptybreach.slug + "/edit/dcon/",
            data=form_data,
        )
        self.assertEqual(302, response.status_code)
        self.assertTrue(BreachDataController.objects.exists())


class BreachCreateBtlViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-empty-kuno.json",
    ]

    def setUp(self):
        self.client = Client()
        self.emptybreach = Breach.objects.get(pk="1")

    def test_createbtlview_template(self):
        self.client.login(username="kuno", password="kuno")
        response = self.client.get(
            "/breach/mybreaches/detail/" + self.emptybreach.slug + "/edit/btl/"
        )
        self.assertTemplateUsed(response, "breach/breach_create_btl.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, BreachCreateBtlView)

    def test_createbtlview_create(self):
        testuser = User.objects.get(pk="2")
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
        self.client.force_login(testuser)
        response = self.client.post(
            "/breach/mybreaches/detail/" + self.emptybreach.slug + "/edit/btl/",
            data=form_data,
        )
        self.assertEqual(302, response.status_code)
        self.assertTrue(BreachTimeLine.objects.exists())


class BreachCreateBdescViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-empty-kuno.json",
    ]

    def setUp(self):
        self.client = Client()
        self.emptybreach = Breach.objects.get(pk="1")

    def test_createbdescview_template(self):
        self.client.login(username="kuno", password="kuno")
        response = self.client.get(
            "/breach/mybreaches/detail/" + self.emptybreach.slug + "/edit/bdesc/"
        )
        self.assertTemplateUsed(response, "breach/breach_create_bdesc.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, BreachCreateBdescView)

    def test_createbdescview_create(self):
        testuser = User.objects.get(pk="2")
        form_data = {
            "bdesc_selection": [
                "lost_device",
            ],
            "bdesc_selection_other": "Some other incident.",
            "bdesc_description": "Some description.",
        }
        self.client.force_login(testuser)
        response = self.client.post(
            "/breach/mybreaches/detail/" + self.emptybreach.slug + "/edit/bdesc/",
            data=form_data,
        )
        self.assertEqual(302, response.status_code)
        self.assertTrue(BreachDescription.objects.exists())


class BreachCreateBaffdViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-empty-kuno.json",
    ]

    def setUp(self):
        self.client = Client()
        self.emptybreach = Breach.objects.get(pk="1")

    def test_createbaffdview_template(self):
        self.client.login(username="kuno", password="kuno")
        response = self.client.get(
            "/breach/mybreaches/detail/" + self.emptybreach.slug + "/edit/baffd/"
        )
        self.assertTemplateUsed(response, "breach/breach_create_baffd.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, BreachCreateBaffdView)

    def test_createbaffdview_create(self):
        testuser = User.objects.get(pk="2")
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
        self.client.force_login(testuser)
        response = self.client.post(
            "/breach/mybreaches/detail/" + self.emptybreach.slug + "/edit/baffd/",
            data=form_data,
        )
        self.assertEqual(302, response.status_code)
        self.assertTrue(BreachAffectedData.objects.exists())


class BreachCreateBaffsViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-empty-kuno.json",
    ]

    def setUp(self):
        self.client = Client()
        self.emptybreach = Breach.objects.get(pk="1")

    def test_createbaffsview_template(self):
        self.client.login(username="kuno", password="kuno")
        response = self.client.get(
            "/breach/mybreaches/detail/" + self.emptybreach.slug + "/edit/baffs/"
        )
        self.assertTemplateUsed(response, "breach/breach_create_baffs.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, BreachCreateBaffsView)

    def test_createbaffsview_create(self):
        testuser = User.objects.get(pk="2")
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
        self.client.force_login(testuser)
        response = self.client.post(
            "/breach/mybreaches/detail/" + self.emptybreach.slug + "/edit/baffs/",
            data=form_data,
        )
        self.assertEqual(302, response.status_code)
        self.assertTrue(BreachAffectedSubjects.objects.exists())


class BreachCreateBconsViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-empty-kuno.json",
    ]

    def setUp(self):
        self.client = Client()
        self.emptybreach = Breach.objects.get(pk="1")

    def test_createbconsview_template(self):
        self.client.login(username="kuno", password="kuno")
        response = self.client.get(
            "/breach/mybreaches/detail/" + self.emptybreach.slug + "/edit/bcons/"
        )
        self.assertTemplateUsed(response, "breach/breach_create_bcons.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, BreachCreateBconsView)

    def test_createbconsview_create(self):
        testuser = User.objects.get(pk="2")
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
        self.client.force_login(testuser)
        response = self.client.post(
            "/breach/mybreaches/detail/" + self.emptybreach.slug + "/edit/bcons/",
            data=form_data,
        )
        self.assertEqual(302, response.status_code)
        self.assertTrue(BreachConsequences.objects.exists())


class BreachCreateBmeasuresViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-empty-kuno.json",
    ]

    def setUp(self):
        self.client = Client()
        self.emptybreach = Breach.objects.get(pk="1")

    def test_createbmeasuresview_template(self):
        self.client.login(username="kuno", password="kuno")
        response = self.client.get(
            "/breach/mybreaches/detail/" + self.emptybreach.slug + "/edit/bmeasures/"
        )
        self.assertTemplateUsed(response, "breach/breach_create_bmeasures.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(
            response.resolver_match.func.view_class, BreachCreateBmeasuresView
        )

    def test_createbmeasuresview_create(self):
        testuser = User.objects.get(pk="2")
        form_data = {
            "bmeasures_taken": "Some measures taken.",
            "bmeasures_proposed": "Some measures proposed.",
            "bmeasures_no_measures_reason": "",
        }
        self.client.force_login(testuser)
        response = self.client.post(
            "/breach/mybreaches/detail/" + self.emptybreach.slug + "/edit/bmeasures/",
            data=form_data,
        )
        self.assertEqual(302, response.status_code)
        self.assertTrue(BreachMeasures.objects.exists())


class BreachCreateBcommViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-empty-kuno.json",
    ]

    def setUp(self):
        self.client = Client()
        self.emptybreach = Breach.objects.get(pk="1")

    def test_createbcommview_template(self):
        self.client.login(username="kuno", password="kuno")
        response = self.client.get(
            "/breach/mybreaches/detail/" + self.emptybreach.slug + "/edit/bcomm/"
        )
        self.assertTemplateUsed(response, "breach/breach_create_bcomm.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, BreachCreateBcommView)

    def test_createbcommview_create(self):
        testuser = User.objects.get(pk="2")
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
        self.client.force_login(testuser)
        response = self.client.post(
            "/breach/mybreaches/detail/" + self.emptybreach.slug + "/edit/bcomm/",
            data=form_data,
        )
        self.assertEqual(302, response.status_code)
        self.assertTrue(BreachCommunication.objects.exists())


class BreachEditDataTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-complete.json",
    ]

    def setUp(self):
        self.client = Client()
        self.completebreach = Breach.objects.get(pk="1")
        self.old_report_update = self.completebreach.report_update

    def test_createbcommview_update(self):
        """Test whether a model instance can be successfully updated
        and report_update is updated accordingly. Use
        BreachCommunication as representative example.
        """
        testuser = User.objects.get(pk="2")
        form_data = {
            "bcomm_communication_selection": "already_happened",
            "bcomm_no_communication_reason": "",
            "bcomm_modality_selection": [
                "publication",
            ],
            "bcomm_modality": "",
            "bcomm_number_of_data_subjects": "",
            "bcomm_remarks": "Some different remarks.",
        }
        self.client.force_login(testuser)
        response = self.client.get(
            "/breach/mybreaches/detail/" + self.completebreach.slug + "/edit/bcomm/"
        )
        self.assertContains(
            response, "form", count=None, status_code=200, msg_prefix="", html=False
        )
        self.assertEqual(
            response.context["form"].initial["bcomm_remarks"], "Some remarks."
        )
        response = self.client.post(
            "/breach/mybreaches/detail/" + self.completebreach.slug + "/edit/bcomm/",
            data=form_data,
        )
        self.assertEqual(302, response.status_code)
        self.assertTrue(BreachCommunication.objects.exists())
        breachcomm = BreachCommunication.objects.get(pk="1")
        self.assertEqual(breachcomm.bcomm_remarks, "Some different remarks.")
        changed_breach = Breach.objects.get(pk="1")
        new_report_update = changed_breach.report_update
        self.assertTrue(new_report_update > self.old_report_update)

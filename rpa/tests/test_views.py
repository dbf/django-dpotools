import datetime
from io import BytesIO

from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from PyPDF2 import PdfReader

from rpa.views import (
    RPAHintsView,
    MyRPAsView,
    AllRPAsView,
    RPADetailView,
    RPADetailPDFView,
    AllRPADeleteView,
    RPAEditView,
    RPACreateView,
    RPACreateRpanmView,
    RPACreateCpdView,
    RPACreateDSubView,
)

from rpa.models import (
    Rpa,
    ProcessingActivityName,
    CategoryOfPersonalData,
    CategoriesOfPersonalDataOrigin,
    DataSubject,
)


class RPAHintsViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
    ]

    def setUp(self):
        self.client = Client()

    def test_rpa_hints_template(self):
        """Test whether RPA hints page is correctly presented to logged
        in user.
        """
        self.client.login(username="kuno", password="kuno")
        response = self.client.get(reverse("rpa:rpa_hints"))
        self.assertTemplateUsed(response, "rpa/rpa_hints.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, RPAHintsView)


class MyRPAsViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-empty-kuno.json",
    ]

    def setUp(self):
        self.client = Client()
        self.emptyrpa = Rpa.objects.get(pk="1")

    def test_rpa_myrpas_visible_to_superuser(self):
        testuser = User.objects.get(pk="1")
        self.client.force_login(testuser)
        self.assertTrue(testuser.is_superuser)
        response = self.client.get(reverse("rpa:my_rpas"))
        self.assertTemplateUsed(response, "rpa/rpa_view.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, MyRPAsView)

    def test_rpa_myrpas_visible_to_dpo(self):
        testuser = User.objects.get(pk="3")
        self.client.force_login(testuser)
        self.assertTrue(testuser.is_staff)
        self.assertTrue(testuser.groups.filter(name="dpo").exists())
        response = self.client.get(reverse("rpa:my_rpas"))
        self.assertTemplateUsed(response, "rpa/rpa_view.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, MyRPAsView)

    def test_rpa_myrpas_visible_to_user(self):
        testuser = User.objects.get(pk="2")
        self.client.force_login(testuser)
        self.assertFalse(testuser.is_superuser)
        self.assertFalse(testuser.is_staff)
        response = self.client.get(reverse("rpa:my_rpas"))
        self.assertTemplateUsed(response, "rpa/rpa_view.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, MyRPAsView)

    def test_rpa_myrpas_user_without_rpa_and_full_name(self):
        testuser_without_fn = User.objects.create_user(
            username="ottokar", password="ottokar"
        )
        self.client.force_login(testuser_without_fn)
        self.assertFalse(testuser_without_fn.is_superuser)
        self.assertFalse(testuser_without_fn.is_staff)
        response = self.client.get(reverse("rpa:my_rpas"))
        self.assertTemplateUsed(response, "rpa/rpa_view.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, MyRPAsView)
        self.assertContains(response, "No RPAs available.")


class AllRPAsViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-empty-kuno.json",
    ]

    def setUp(self):
        self.client = Client()
        self.emptyrpa = Rpa.objects.get(pk="1")

    def test_rpa_allrpas_visible_to_superuser(self):
        testuser = User.objects.get(pk="1")
        self.client.force_login(testuser)
        self.assertTrue(testuser.is_superuser)
        response = self.client.get(reverse("rpa:all_rpas"))
        self.assertTemplateUsed(response, "rpa/rpa_view_all.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, AllRPAsView)

    def test_rpa_allrpas_visible_to_dpo(self):
        testuser = User.objects.get(pk="3")
        self.client.force_login(testuser)
        self.assertTrue(testuser.is_staff)
        self.assertTrue(testuser.groups.filter(name="dpo").exists())
        response = self.client.get(reverse("rpa:all_rpas"))
        self.assertTemplateUsed(response, "rpa/rpa_view_all.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, AllRPAsView)

    def test_rpa_allrpas_denied_to_user(self):
        testuser = User.objects.get(pk="2")
        self.client.force_login(testuser)
        self.assertFalse(testuser.is_superuser)
        self.assertFalse(testuser.is_staff)
        response = self.client.get(reverse("rpa:all_rpas"))
        self.assertEqual(response.status_code, 403)

    def test_rpa_allrpas_empty_list_shown(self):
        testuser = User.objects.get(pk="3")
        self.client.force_login(testuser)
        self.assertTrue(testuser.is_staff)
        self.assertTrue(testuser.groups.filter(name="dpo").exists())
        self.emptyrpa.delete()
        response = self.client.get(reverse("rpa:all_rpas"))
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, AllRPAsView)
        self.assertContains(response, "No RPAs available.")


class RPADetailViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete.json",
        "testrpa-empty-hugo.json",
    ]

    def setUp(self):
        self.client = Client()

    def test_rpa_detail_user_own(self):
        """Test whether non-privileged users can detail view their own
        RPAs.
        """
        testuser = User.objects.get(pk="2")
        self.client.force_login(testuser)
        ownrpa = Rpa.objects.get(pk="1")
        reference = ownrpa.slug
        response = self.client.get("/rpa/myrpas/detail/" + ownrpa.slug + "/")
        self.assertTemplateUsed(response, "rpa/rpa_htmltemplate.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reference)
        self.assertIs(response.resolver_match.func.view_class, RPADetailView)

    def test_rpa_detail_user_other(self):
        """Test whether non-privileged users can detail view RPAs
        of other users. Should result in 403.
        """
        testuser = User.objects.get(pk="2")
        self.client.force_login(testuser)
        otherrpa = Rpa.objects.get(pk="2")
        response = self.client.get("/rpa/myrpas/detail/" + otherrpa.slug + "/")
        self.assertEqual(response.status_code, 403)

    def test_rpa_detail_su_other(self):
        """Test whether superusers can detail view RPAs of other users."""
        testuser = User.objects.get(pk="1")
        self.client.force_login(testuser)
        otherrpa = Rpa.objects.get(pk="1")
        reference = otherrpa.slug
        response = self.client.get("/rpa/myrpas/detail/" + otherrpa.slug + "/")
        self.assertTemplateUsed(response, "rpa/rpa_htmltemplate.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reference)
        self.assertIs(response.resolver_match.func.view_class, RPADetailView)

    def test_rpa_detail_dpo_other(self):
        """Test whether dpo users can detail view RPAs of other users."""
        testuser = User.objects.get(pk="3")
        self.client.force_login(testuser)
        otherrpa = Rpa.objects.get(pk="1")
        reference = otherrpa.slug
        response = self.client.get("/rpa/myrpas/detail/" + otherrpa.slug + "/")
        self.assertTemplateUsed(response, "rpa/rpa_htmltemplate.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reference)


class RPADetailPDFViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-empty-kuno.json",
        "testrpa-empty-hugo.json",
    ]

    def setUp(self):
        self.client = Client()

    def test_rpa_detail_pdf_user_own(self):
        """Test whether non-privileged users can detail view their own
        RPAs (PDF export).
        """
        testuser = User.objects.get(pk="2")
        self.client.force_login(testuser)
        ownrpa = Rpa.objects.get(pk="1")
        reference = ownrpa.slug
        response = self.client.get("/rpa/myrpas/detail/" + ownrpa.slug + "/pdf/")
        file = BytesIO()
        file.write(response.content)
        file.seek(0)
        reader = PdfReader(file)
        page = reader.pages[0]
        text = page.extract_text()
        self.assertTemplateUsed(response, "rpa/rpa_pdftemplate.html")
        self.assertEqual(response.status_code, 200)
        # reference string should be on 1st page of pdf
        self.assertTrue(reference in text)
        self.assertIs(response.resolver_match.func.view_class, RPADetailPDFView)

    def test_rpa_detail_pdf_filename(self):
        """Test whether filename for PDF export will be set correctly."""
        testuser = User.objects.get(pk="2")
        self.client.force_login(testuser)
        ownrpa = Rpa.objects.get(pk="1")
        response = self.client.get("/rpa/myrpas/detail/" + ownrpa.slug + "/pdf/")
        content_disp = response["Content-Disposition"]
        expectedfn = (
            "rpa-"
            + ownrpa.slug
            + "-"
            + str(datetime.date.today().strftime("%Y%m%d"))
            + ".pdf"
        )
        self.assertTrue(expectedfn in content_disp)

    def test_rpa_detail_pdf_user_other(self):
        """Test whether non-privileged users can detail view RPAs
        of other users (pdf export). Should result in 403.
        """
        testuser = User.objects.get(pk="2")
        self.client.force_login(testuser)
        otherrpa = Rpa.objects.get(pk="2")
        response = self.client.get("/rpa/myrpas/detail/" + otherrpa.slug + "/pdf/")
        self.assertEqual(response.status_code, 403)


class AllRPADeleteViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-empty-kuno.json",
    ]

    def setUp(self):
        self.client = Client()
        self.emptyrpa = Rpa.objects.get(pk="1")

    def test_rpa_allrpas_delete_visible_to_superuser(self):
        testuser = User.objects.get(pk="1")
        self.client.force_login(testuser)
        self.assertTrue(testuser.is_superuser)
        response = self.client.get(
            "/rpa/allrpas/detail/" + self.emptyrpa.slug + "/delete/"
        )
        self.assertTemplateUsed(response, "rpa/rpa_delete_confirmation.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, AllRPADeleteView)

    def test_rpa_allrpas_delete_visible_to_dpo(self):
        testuser = User.objects.get(pk="3")
        self.client.force_login(testuser)
        self.assertTrue(testuser.is_staff)
        response = self.client.get(
            "/rpa/allrpas/detail/" + self.emptyrpa.slug + "/delete/"
        )
        self.assertTemplateUsed(response, "rpa/rpa_delete_confirmation.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, AllRPADeleteView)

    def test_rpa_allrpas_delete_denied_to_user(self):
        testuser = User.objects.get(pk="2")
        self.client.force_login(testuser)
        self.assertFalse(testuser.is_superuser)
        self.assertFalse(testuser.is_staff)
        response = self.client.get(
            "/rpa/allrpas/detail/" + self.emptyrpa.slug + "/delete/"
        )
        self.assertEqual(response.status_code, 403)


class RPAEditViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-empty-kuno.json",
    ]

    def setUp(self):
        self.client = Client()
        self.emptyrpa = Rpa.objects.get(pk="1")

    def test_edit_view_template(self):
        self.client.login(username="kuno", password="kuno")
        response = self.client.get(
            "/rpa/myrpas/detail/" + self.emptyrpa.slug + "/edit/"
        )
        self.assertTemplateUsed(response, "rpa/rpa_edit.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, RPAEditView)
        self.assertContains(response, "<th>Acronym</th>", html=True)


class RPACreateViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
    ]

    def setUp(self):
        self.client = Client()

    def test_createview_template(self):
        """Test whether RPACreateView is correctly presented to logged
        in user.
        """
        self.client.login(username="kuno", password="kuno")
        response = self.client.get(reverse("rpa:rpa_create"))
        self.assertTemplateUsed(response, "rpa/rpa_create_slug.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, RPACreateView)

    def test_createview_create(self):
        testuser = User.objects.get(pk="2")
        form_data = {
            "user": 2,
            "slug": "testrpa1",
            "rpa_bumper": True,
            "helptext_display_default": "show",
        }
        self.client.force_login(testuser)
        response = self.client.post(reverse("rpa:rpa_create"), data=form_data)
        self.assertEqual(302, response.status_code)
        self.assertTrue(Rpa.objects.exists())


class RPACreateRpanmViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-empty-kuno.json",
    ]

    def setUp(self):
        self.client = Client()
        self.emptyrpa = Rpa.objects.get(pk="1")

    def test_create_rpanm_view_template(self):
        self.client.login(username="kuno", password="kuno")
        response = self.client.get(
            "/rpa/myrpas/detail/" + self.emptyrpa.slug + "/edit/rpanm/"
        )
        self.assertTemplateUsed(response, "rpa/rpa_create_name.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, RPACreateRpanmView)

    def test_create_rpanm_view_create(self):
        testuser = User.objects.get(pk="2")
        form_data = {
            "name": "Some RPA descriptive name",
            "is_new": True,
            "date_intro": "2022-12-12",
        }
        self.client.force_login(testuser)
        response = self.client.post(
            "/rpa/myrpas/detail/" + self.emptyrpa.slug + "/edit/rpanm/",
            data=form_data,
        )
        self.assertEqual(302, response.status_code)
        self.assertTrue(ProcessingActivityName.objects.exists())


class RPACreateCpdViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-empty-kuno.json",
    ]

    def setUp(self):
        self.client = Client()
        self.emptyrpa = Rpa.objects.get(pk="1")

    def test_createcpdview_template(self):
        self.client.login(username="kuno", password="kuno")
        response = self.client.get(
            "/rpa/myrpas/detail/" + self.emptyrpa.slug + "/edit/cpd/"
        )
        self.assertTemplateUsed(response, "rpa/rpa_create_cpd.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, RPACreateCpdView)

    def test_createcpdview_create(self):
        # https://stackoverflow.com/questions/1630754/django-formset-unit-test
        def create_formset_post_data(response, new_form_data=None):
            if new_form_data is None:
                new_form_data = []
            csrf_token = response.context["csrf_token"]
            formset = response.context["formset"]
            prefix_template = formset.empty_form.prefix
            management_form_data = formset.management_form.initial
            form_data_list = formset.initial
            if form_data_list is None:
                form_data_list = []
            form_data_list.extend(new_form_data)
            management_form_data["TOTAL_FORMS"] = len(form_data_list)
            post_data = dict(csrf_token=csrf_token)
            for key, value in management_form_data.items():
                prefix = prefix_template.replace("__prefix__", "")
                post_data[prefix + key] = value
            for index, form_data in enumerate(form_data_list):
                for key, value in form_data.items():
                    prefix = prefix_template.replace("__prefix__", f"{index}-")
                    post_data[prefix + key] = value
            return post_data

        testuser = User.objects.get(pk="2")
        self.client.force_login(testuser)
        response = self.client.get(
            "/rpa/myrpas/detail/" + self.emptyrpa.slug + "/edit/cpd/"
        )
        self.assertEqual(response.status_code, 200)
        formset_data = [
            dict(cpd_index=1, cpd_name="Name", cpd_is_special=False),
            dict(cpd_index=2, cpd_name="Postal address", cpd_is_special=False),
            dict(cpd_index=3, cpd_name="Trade union membership", cpd_is_special=True),
        ]
        post_data = create_formset_post_data(response, new_form_data=formset_data)
        response = self.client.post(
            "/rpa/myrpas/detail/" + self.emptyrpa.slug + "/edit/cpd/",
            data=post_data,
        )
        self.assertEqual(302, response.status_code)
        self.assertTrue(CategoryOfPersonalData.objects.exists())
        rpacpd = CategoryOfPersonalData.objects.filter(cpd_index=3).get()
        self.assertEqual(rpacpd.cpd_name, "Trade union membership")


class RPACreateDSubViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-cpd-kuno.json",
    ]

    def setUp(self):
        self.client = Client()
        self.rpawithcpd = Rpa.objects.get(pk="42")

    def test_createdsubview_template(self):
        self.client.login(username="kuno", password="kuno")
        response = self.client.get(
            "/rpa/myrpas/detail/" + self.rpawithcpd.slug + "/edit/dsub/"
        )
        self.assertTemplateUsed(response, "rpa/rpa_create_dsub.html")
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.resolver_match.func.view_class, RPACreateDSubView)

    def test_createdsubview_create(self):
        # https://stackoverflow.com/questions/1630754/django-formset-unit-test
        def create_formset_post_data(response, new_form_data=None):
            if new_form_data is None:
                new_form_data = []
            csrf_token = response.context["csrf_token"]
            formset = response.context["formset"]
            prefix_template = formset.empty_form.prefix
            management_form_data = formset.management_form.initial
            form_data_list = formset.initial
            if form_data_list is None:
                form_data_list = []
            form_data_list.extend(new_form_data)
            management_form_data["TOTAL_FORMS"] = len(form_data_list)
            post_data = dict(csrf_token=csrf_token)
            for key, value in management_form_data.items():
                prefix = prefix_template.replace("__prefix__", "")
                post_data[prefix + key] = value
            for index, form_data in enumerate(form_data_list):
                for key, value in form_data.items():
                    prefix = prefix_template.replace("__prefix__", f"{index}-")
                    post_data[prefix + key] = value
            return post_data

        testuser = User.objects.get(pk="2")
        self.client.force_login(testuser)
        response = self.client.get(
            "/rpa/myrpas/detail/" + self.rpawithcpd.slug + "/edit/dsub/"
        )
        self.assertEqual(response.status_code, 200)
        formset_data = [
            dict(
                dsub_name="Some data subj cat #1",
                dsub_cpd_sel=[
                    1,
                    2,
                ],
            ),
            dict(
                dsub_name="Some data subj cat #2",
                dsub_cpd_sel=[
                    2,
                ],
            ),
            dict(
                dsub_name="Some data subj cat #3",
                dsub_cpd_sel=[
                    2,
                    3,
                ],
            ),
        ]
        post_data = create_formset_post_data(response, new_form_data=formset_data)
        response = self.client.post(
            "/rpa/myrpas/detail/" + self.rpawithcpd.slug + "/edit/dsub/",
            data=post_data,
        )
        self.assertEqual(302, response.status_code)
        self.assertTrue(DataSubject.objects.exists())
        rpadsub = DataSubject.objects.filter(
            dsub_name="Some data subj cat #3"
        ).prefetch_related("cpd")
        rpadsub_cpd = CategoryOfPersonalData.objects.filter(datasubjects__in=rpadsub)
        expected_dsub_cpd = "2 3"
        actual_dsub_cpd = (
            str(rpadsub_cpd[0].cpd_index) + " " + str(rpadsub_cpd[1].cpd_index)
        )
        self.assertEqual(actual_dsub_cpd, expected_dsub_cpd)


class RpaEditDataSimpleFormViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete.json",
    ]

    def setUp(self):
        self.client = Client()
        self.completerpa = Rpa.objects.get(pk="1")

    def test_update_cpdo(self):
        """Test whether a model instance can be successfully updated.
        Use CategoriesOfPersonalDataOrigin as example.
        """
        testuser = User.objects.get(pk="2")
        form_data = {
            "cpdo_descr": "Some data origin",
        }
        self.client.force_login(testuser)
        response = self.client.get(
            "/rpa/myrpas/detail/" + self.completerpa.slug + "/edit/cpdo/"
        )
        self.assertContains(
            response, "form", count=None, status_code=200, msg_prefix="", html=False
        )
        self.assertEqual(
            response.context["form"].initial["cpdo_descr"], "Data subjects themselves"
        )
        response = self.client.post(
            "/rpa/myrpas/detail/" + self.completerpa.slug + "/edit/cpdo/",
            data=form_data,
        )
        self.assertEqual(302, response.status_code)
        self.assertTrue(CategoriesOfPersonalDataOrigin.objects.exists())
        self.completerpa.refresh_from_db()
        rpacpdo = CategoriesOfPersonalDataOrigin.objects.get(pk="1")
        self.assertEqual(rpacpdo.cpdo_descr, "Some data origin")


class RpaEditDataChoiceFormsetViewTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete.json",
    ]

    def setUp(self):
        self.client = Client()
        self.completerpa = Rpa.objects.get(pk="1")

    def test_update_cpdo(self):
        """Test whether a model instance can be successfully updated.
        Use CategoryOfRecipients as example.
        """
        testuser = User.objects.get(pk="2")
        form_data = {
            "cpdo_descr": "Some data origin",
        }
        self.client.force_login(testuser)
        response = self.client.get(
            "/rpa/myrpas/detail/" + self.completerpa.slug + "/edit/cpdo/"
        )
        self.assertContains(
            response, "form", count=None, status_code=200, msg_prefix="", html=False
        )
        self.assertEqual(
            response.context["form"].initial["cpdo_descr"], "Data subjects themselves"
        )
        response = self.client.post(
            "/rpa/myrpas/detail/" + self.completerpa.slug + "/edit/cpdo/",
            data=form_data,
        )
        self.assertEqual(302, response.status_code)
        self.assertTrue(CategoriesOfPersonalDataOrigin.objects.exists())
        self.completerpa.refresh_from_db()
        rpacpdo = CategoriesOfPersonalDataOrigin.objects.get(pk="1")
        self.assertEqual(rpacpdo.cpdo_descr, "Some data origin")


class RPADetailViewWithDPOCommentsTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete-with-dpoc.json",
    ]

    def setUp(self):
        self.client = Client()
        self.rpa_with_dpoc = Rpa.objects.get(pk="1")

    def test_dpoc_in_html_doc(self):
        """Test whether DPO comments are shown in HTML document view
        (18 models have comment option).
        """
        testuser = User.objects.get(pk="2")
        self.client.force_login(testuser)
        response = self.client.get(
            "/rpa/myrpas/detail/" + self.rpa_with_dpoc.slug + "/"
        )
        self.assertContains(
            response,
            "Your RPA is not finished",
            count=18,
            status_code=200,
            msg_prefix="",
            html=False,
        )

    def test_remove_dpoc_from_html_doc(self):
        """Test whether DPO comment removal from HTML document view
        works (18-1=17).
        """
        testuser = User.objects.get(pk="2")
        form_data = {
            "name": "Test-RPA complete minimal",
            "is_new": True,
            "date_intro": "2022-12-15",
            "dpo_comment": "",
        }
        self.client.force_login(testuser)
        response = self.client.post(
            "/rpa/myrpas/detail/" + self.rpa_with_dpoc.slug + "/edit/rpanm/",
            data=form_data,
        )
        self.assertEqual(302, response.status_code)
        self.rpa_with_dpoc.refresh_from_db()
        response = self.client.get(
            "/rpa/myrpas/detail/" + self.rpa_with_dpoc.slug + "/"
        )
        self.assertContains(
            response,
            "Your RPA is not finished",
            count=17,
            status_code=200,
            msg_prefix="",
            html=False,
        )


class RPAEditViewWithDPOCommentsTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete-with-dpoc.json",
    ]

    def setUp(self):
        self.client = Client()
        self.rpa_with_dpoc = Rpa.objects.get(pk="1")

    def test_dpoc_in_edit_view(self):
        """Test whether DPO comments are shown in edit view (18 models
        have comment option).
        """
        testuser = User.objects.get(pk="2")
        self.client.force_login(testuser)
        response = self.client.get(
            "/rpa/myrpas/detail/" + self.rpa_with_dpoc.slug + "/edit/"
        )
        self.assertContains(
            response,
            "present, check",
            count=19,  # 18+1 in helptext
            status_code=200,
            msg_prefix="",
            html=False,
        )

    def test_remove_dpoc_from_edit_view(self):
        """Test whether DPO comment removal from edit view works
        (18-1=17).
        """
        testuser = User.objects.get(pk="2")
        form_data = {
            "name": "Test-RPA complete minimal",
            "is_new": True,
            "date_intro": "2022-12-15",
            "dpo_comment": "",
        }
        self.client.force_login(testuser)
        response = self.client.post(
            "/rpa/myrpas/detail/" + self.rpa_with_dpoc.slug + "/edit/rpanm/",
            data=form_data,
        )
        self.assertEqual(302, response.status_code)
        self.rpa_with_dpoc.refresh_from_db()
        response = self.client.get(
            "/rpa/myrpas/detail/" + self.rpa_with_dpoc.slug + "/edit/"
        )
        self.assertContains(
            response,
            "present, check",
            count=18,  # 18+1 in helptext -1 removed
            status_code=200,
            msg_prefix="",
            html=False,
        )

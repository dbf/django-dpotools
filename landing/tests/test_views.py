from django.contrib.auth.models import User
from django.test import TestCase, Client, override_settings
from django.urls import reverse


class LandingViewsTest(TestCase):
    """Test whether landing views work and use correct templates."""

    def test_alive(self):
        response = self.client.get(reverse("landing:alive"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing/alive.html")
        self.assertContains(response, "alive")

    def test_home(self):
        response = self.client.get(reverse("landing:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dpotools.html")
        self.assertTemplateUsed(response, "landing/landing.html")
        self.assertContains(response, "DPO tool")

    @override_settings(LANGUAGE_CODE="de", LANGUAGES=(("de", "German"),))
    def test_lang_german(self):
        response = self.client.get(reverse("landing:home"))
        self.assertContains(response, "DSB")
        self.assertContains(response, "Datenschutz")


class DpoToolsMainTemplateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.testuser = User.objects.create_user(username="ottokar", password="ottokar")

    def test_user_without_full_name(self):
        """Test whether dpotools main template shows rpa and breach
        menues for logged in users.
        """
        self.client.force_login(self.testuser)
        response = self.client.get(reverse("landing:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dpotools.html")
        self.assertTemplateUsed(response, "landing/landing.html")
        self.assertContains(response, self.testuser.username)
        self.assertContains(
            response,
            '<button class="btn btn-primary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">RPA generator</button>',
            html=True,
        )
        self.assertContains(
            response,
            '<button class="btn btn-primary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Breach reporter</button>',
            html=True,
        )

    def test_anonymous_user(self):
        """Test whether dpotools main template doesn't show rpa and
        breach menues for anonymous users.
        """
        response = self.client.get(reverse("landing:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dpotools.html")
        self.assertTemplateUsed(response, "landing/landing.html")
        self.assertContains(response, "Not logged in.")
        self.assertNotContains(
            response,
            '<button class="btn btn-primary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">RPA generator</button>',
            html=True,
        )
        self.assertNotContains(
            response,
            '<button class="btn btn-primary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Breach reporter</button>',
            html=True,
        )

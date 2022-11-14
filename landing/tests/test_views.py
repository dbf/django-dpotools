from django.test import TestCase, override_settings
from django.urls import reverse


class LandingViewsTest(TestCase):
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

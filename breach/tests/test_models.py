from django.test import TestCase

from breach.models import (
    Breach,
)


class BreachModelsStrTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testbreach-complete.json",
    ]

    def setUp(self):
        self.completebreach = Breach.objects.get(pk="1")

    def test_model_strs(self):
        self.assertEqual(
            str(self.completebreach),
            "complete-breach",
        )
        self.assertEqual(
            str(self.completebreach.datacontrollers.filter().first()),
            "complete-breach data controller",
        )
        self.assertEqual(
            str(self.completebreach.timelines.filter().first()),
            "complete-breach time line",
        )
        self.assertEqual(
            str(self.completebreach.descriptions.filter().first()),
            "complete-breach description",
        )
        self.assertEqual(
            str(self.completebreach.affected_data.filter().first()),
            "complete-breach affected data",
        )
        self.assertEqual(
            str(self.completebreach.affected_subjects.filter().first()),
            "complete-breach affected subjects",
        )
        self.assertEqual(
            str(self.completebreach.consequences.filter().first()),
            "complete-breach consequences",
        )
        self.assertEqual(
            str(self.completebreach.measures.filter().first()),
            "complete-breach measures",
        )
        self.assertEqual(
            str(self.completebreach.communications.filter().first()),
            "complete-breach communication",
        )

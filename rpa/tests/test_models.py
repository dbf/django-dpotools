from django.test import TestCase

from rpa.models import (
    Rpa,
)


class RpaModelsStrTest(TestCase):
    fixtures = [
        "models-users-groups-permissions.json",
        "testrpa-complete.json",
    ]

    def setUp(self):
        self.completerpa = Rpa.objects.get(pk=1)

    def test_model_strs(self):
        """Test whether models str methods return correct strings."""
        self.assertEqual(
            str(self.completerpa),
            "complete-rpa",
        )
        self.assertEqual(
            str(self.completerpa.rpa_names.filter().first()),
            "complete-rpa RPA designation",
        )
        self.assertEqual(
            str(self.completerpa.datacontrollers.filter().first()),
            "complete-rpa data controller",
        )
        self.assertEqual(
            str(self.completerpa.jointcontrollers.filter().first()),
            "complete-rpa joint controller",
        )
        self.assertEqual(
            str(self.completerpa.dpos.filter().first()),
            "complete-rpa dpo",
        )
        self.assertEqual(
            str(self.completerpa.internally_resp_depts.filter().first()),
            "complete-rpa internally resp.",
        )
        self.assertEqual(
            str(self.completerpa.datacategories.filter().first()),
            "complete-rpa data categories",
        )
        self.assertEqual(
            str(self.completerpa.datacategories_origin.filter().first()),
            "complete-rpa data categories origin",
        )
        self.assertEqual(
            str(self.completerpa.purposes_legalbases.filter().first()),
            "complete-rpa purpose/legal basis",
        )
        self.assertEqual(
            str(self.completerpa.datasubjects.filter().first()),
            "complete-rpa data subjects",
        )
        self.assertEqual(
            str(self.completerpa.timelimits_erasure.filter().first()),
            "complete-rpa erasure limits",
        )
        self.assertEqual(
            str(self.completerpa.categories_of_rec.filter().first()),
            "complete-rpa Cat. of recipients",
        )
        self.assertEqual(
            str(self.completerpa.transfers_to_3rdc.filter().first()),
            "complete-rpa transfer to 3rd c.",
        )
        self.assertEqual(
            str(self.completerpa.accessgroups.filter().first()),
            "complete-rpa access groups",
        )
        self.assertEqual(
            str(self.completerpa.transparencies.filter().first()),
            "complete-rpa transparency",
        )
        self.assertEqual(
            str(self.completerpa.dataprocessors.filter().first()),
            "complete-rpa data processor",
        )
        self.assertEqual(
            str(self.completerpa.pias.filter().first()),
            "complete-rpa PIA",
        )
        self.assertEqual(
            str(self.completerpa.toms.filter().first()),
            "complete-rpa TOM",
        )
        self.assertEqual(
            str(self.completerpa.rpa_annexes.filter().first()),
            "complete-rpa RPA annex",
        )

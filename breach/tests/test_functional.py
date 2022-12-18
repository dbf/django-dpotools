from django_webtest import WebTest

from breach.models import (
    Breach,
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

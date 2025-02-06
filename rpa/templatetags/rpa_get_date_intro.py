from django.template.defaulttags import register
from django.utils.dateformat import DateFormat
from django.utils.translation import gettext_lazy as _


@register.filter
def rpa_get_date_intro(rpa):
    """Used to get RPA date_intro/date_changed in the view and view_all templates"""
    chgd = _("chgd.")
    retval = ""
    try:
        rpa_date_intro = [
            DateFormat(rpa.date_intro).format("Y-m-d") for rpa in rpa.rpa_names.all()
        ]
        retval = "".join(rpa_date_intro)
    except AttributeError:
        try:
            rpa_date_changed = [
                DateFormat(rpa.date_changed).format("Y-m-d")
                for rpa in rpa.rpa_names.all()
            ]
            retval = "".join(rpa_date_changed) + " (" + chgd + ")"
        except Exception:
            pass
    except Exception:
        pass
    finally:
        return retval

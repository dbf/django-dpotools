# [django-dpotools](https://github.com/dbf/django-dpotools)
## Breach report examples

This directory contains (fictitious) notifications of personal data
breaches (aka breach reports) examples in different languages. Each
example comes as raw data (JSON) and as PDF.

JSON data has been exported using `python manage.py dumpdata` and can be
imported into django-dpotools using `python manage.py loaddata`.

You may want to adjust the user pk in model "breach.breach" to an
existing user's pk before attempting an import.

If the Breach report database tables of your django-dpotools
installation are not empty, you also may want to adjust all breach model
pks to values that are not in use already.

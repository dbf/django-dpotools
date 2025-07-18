# [django-dpotools](https://github.com/dbf/django-dpotools)
django-dpotools is an open source collection of tools meant to simplify
the life of data protection officers (DPOs) of large entities (such as
universities) with a lot of individuals and departments processing
personal data.

django-dpotools currently include
- a form to securely and (as an option) anonymously pass information to
  the DPO; this comes in handy, if encrypted email is unavailable and
  documents need to be passed to the DPO (such as proofs of identity in
  case of exercise of the right of access, Art. 15 GDPR)
- a guided form (basically a single-purpose editor) to create records of
  processing activities (RPAs, Art. 30 GDPR), that is intended to be
  used by individuals or departments processing personal data, tries to
  intercept as many common mistakes as possible and allows the DPO to
  intervene if necessary
- a guided form (basically a single-purpose editor), that allows
  individuals or departments to create notifications of personal data
  breaches (Art. 33 GDPR), that are intended to be revised by the DPO
  and then be forwarded to the competent supervisory authority by the
  DPO acting on behalf of the data controller

Additional guided forms to create other data protection related
documents are currently being discussed in terms of effort vs. benefit.

You are welcome to contribute, preferrably by
- providing translations in EU-languages other than those already
  available (django-dpotools uses the standard Django translation scheme
  that leverages GNU gettext [1]; make sure to use the correct GDPR
  terms in your language) - django-rosetta is probably the tool of
  choice here
- checking the code for issues, security issues in particular
- improving the code for usability, readability and elegance (i am aware
  that this project is clumsy, if not a sorry effort towards the fine
  arts of Python programming and Web design ;-)
- improving testing by checking the tests for redundancies, inaccuracies
  and incomplete coverage; if you consider to contribute code for new
  functionality, make sure to include tests for your contributed code

If at all possible, keep pull requests small, clear and consistently
formatted (black [2] with no options). Please do not make pull requests
for template content (except translations, typos or comprehensibly
debatable information) - at least minor changes to template content will
be required for every individual entity anyway. There's no "one size
fits all".

If you are a DPO and want to try this: Unobtrusively ask your local IT
crowd to provide you with a working installation, preferrably on a
dedicated virtual machine.  If you have Python skills yourself, refer to
the paragraph below. You are explicitly encouraged to carefully check
all templates and help texts, since quite a few of them are either
opinionated or reflect given factors at the fine entity these tools were
developed for (and they simply may contain errors as well).  Please feel
free to suggest enhancements that you would like to see (by opening an
issue), such as additional form fields or choice options (prerequisite:
must be useful for others).

If you are the local IT crowd forced by your DPO to try this: Install
Python 3.9+ on your machine, git clone this repository, create a virtual
environment and pip install the requirements into it. Copy
*local_settings_fake.py* to *local_settings.py* and provide the required
data for your entity. __Carefully review the global *settings.py* as
well.__ django-dpotools is pretty much standard Django,

```
python manage.py makemigrations breach rpa
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

will do. Almost no custom JavaScript, no other fancy stuff (yes, it
looks boring). Some third party packages are required, though.
DPO users need to have "staff" status and belong to Django group "dpo"
in order to be able to access all RPAs and breach reports. This group
needs to be created and provided with sufficient access to RPA and
breach database objects.
JSON dumps with example data and the corresponding PDFs are available in
*examples-rpa* and *examples-breach*.

In order to use translated versions of django-dpotools (currently, only
German is available), a

```
django-admin compilemessages
```

is required.

You may want to further lock down access to the RPA generator and the
breach reporter in production use (the contact app probably makes sense
only, if it is accessible from the internet and therefore your Django
installation will be exposed to all kinds of bad things).
The django-lockdown package and Fail2ban are amongst the options to
achieve this. Bootstrap, jQuery, popper.js and DataTables are included
in order to avoid to force clients to contact third party servers.

Known bugs and limitations:
- RPA generator: One can specify time limits for erasure, categories of
  recipients, etc. by data category only. It is not possible to specify
  by data subject category or both data category and data subject
  category.
- Not all form elements (in the RPA generator TOM form in particular)
  are properly validated in terms of logic, yet (i.e. logically wrong
  combinations of choices are possible).

License (Bootstrap, jQuery, popper.js, DataTables): MIT, for (C) cf. resp. files  
License (django-dpotools): EUPL-1.2 [3]

Similar open source projects that i know of (but did not try yet):
- [Open-Datenschutzcenter](https://github.com/H2-invent/open-datenschutzcenter)
- [GDPR Transparency](https://github.com/BjoernKW/gdpr-transparency)

---

[1] [https://docs.djangoproject.com/en/4.2/topics/i18n/translation/](https://docs.djangoproject.com/en/4.2/topics/i18n/translation/)  
[2] [https://black.readthedocs.io/](https://black.readthedocs.io/)  
[3] [https://www.eupl.eu/](https://www.eupl.eu/)  

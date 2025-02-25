from django.utils.translation import gettext_lazy as _

# entity specific fixed information for sending email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
#EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'dpo@some-entity.org'
#EMAIL_PORT = 587
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''
FILE_UPLOAD_MAX_MEMORY_SIZE = 12582912
DATA_UPLOAD_MAX_MEMORY_SIZE = 13631488

# entity specific fixed information for contact form
CONTACT_RECIPIENT = 'dpo@some-entity.org'
CONTACT_MAX_FILESIZE = 11534336
CONTACT_ALLOWED_MIMETYPES = ['application/pdf', 'image/jpeg', 'image/png', 'text/plain']
CONTACT_SUBJ_PREFIX = _('[DPO CONTACT FORM] ')
CONTACT_EMPTY_SENDER_NAME = _('Anonymous')
CONTACT_EMPTY_SENDER_EMAIL = 'do-not-reply@anonymous.some-entity.org'
CONTACT_WARNING = _("""
************************************************************************
* Warning: This mail was sent via the publicly accessible DPO
* contact form. This contact form allows to enter arbitrary
* information, so be skeptical about the content.
* In case no sender was given, this mail will show "do-not-reply@" as
* sender. Answering to this sender is futile (undeliverable).
* In case this mail has an attachment, save it and check the file
* for possible malware before you open it.
************************************************************************
""")

# entity specific fixed information for templates
CONTROLLER_NAME = _('Some entity')
CONTROLLER_REPBY = _('The President')
CONTROLLER_STREET = _('42 Sesame St.')
CONTROLLER_PCODE = '54321'
CONTROLLER_CITY = _('Some city')
CONTROLLER_COUNTRY = _('Some state')
CONTROLLER_PHONE = '+43 324 657-0'
CONTROLLER_EMAIL = 'president@some-entity.org'
CONTROLLER_MAILDOM = 'some-entity.org'
CONTROLLER_WEB = 'https://www.some-entity.org/'
CONTROLLER_PN = 'https://www.some-entity.org/privacy'
CONTROLLER_HRM = _('Some entity HRM')
DPO_NAME = _('Data Protection Officer')
DPO_STREET = CONTROLLER_STREET
DPO_PCODE = CONTROLLER_PCODE
DPO_CITY = CONTROLLER_CITY
DPO_COUNTRY = CONTROLLER_COUNTRY
DPO_PHONE = '+43 324 657-1234'
DPO_EMAIL = 'dpo@some-entity.org'
DPO_WEB = 'https://www.some-entity.org/go/dpo'
SUPAUTH_NAME = _('The Some state Commissioner for Data Protection')
SUPAUTH_STREET = _('PO Box 4711')
SUPAUTH_PCODE = '12345'
SUPAUTH_CITY = _('Some capital')
SUPAUTH_COUNTRY = _('Some state')
SUPAUTH_PHONE = '+49 867 4242-0'
SUPAUTH_EMAIL = 'pobox@some-states-competent-supauth.some-state.org'
SUPAUTH_WEB = 'https://some-states-competent-supauth.some-state.org/'
SUPAUTH_PIA_REQUIRED_LIST = 'https://some-states-competent-supauth.some-state.org/pia-required-list'
CERT_ISSUED_BY = _('Some CA')
CERT_VALID_UNTIL = '24 Mar 2024'
CERT_FP_SHA1 = '2a:3b:ae:f5:58:86:86:60:b4:f0:43:a3:91:ee:5f:ea:33:75:28:0b'
CERT_FP_SHA256 = '61:18:76:b5:10:18:be:68:5b:a4:a6:4e:6a:ef:83:62:a1:06:eb:ef:2f:3e:a5:fd:9b:31:a2:6b:69:14:a7:b9'
DPO_COMM_COL_PRS = '#60e080'
DPO_COMM_COL_MIS = '#ff6060'
DPO_COMM_COL_CHK = '#ffc107'
DPO_COMM_COL_DEF = '#f8f9fa'
DPO_COMMENT = _("DPO comment")
DPO_COMMENT_HELPTEXT = _("Address the issues described above (optionally add a comment yourself), then check the box and submit the form.")

EMAIL_DPO_ON_NEW_RPA = False
EMAIL_DPO_ON_NEW_BREACHREP = True
EMAIL_ON_NEW_DOC_RECIPIENT = DPO_EMAIL

SETTINGS_EXPORT = [
    'CONTROLLER_NAME', 'CONTROLLER_REPBY', 'CONTROLLER_STREET', 'CONTROLLER_PCODE', 'CONTROLLER_CITY',
    'CONTROLLER_COUNTRY', 'CONTROLLER_PHONE', 'CONTROLLER_EMAIL', 'CONTROLLER_MAILDOM', 'CONTROLLER_WEB',
    'CONTROLLER_PN', 'CONTROLLER_HRM',
    'DPO_NAME', 'DPO_STREET', 'DPO_PCODE', 'DPO_CITY', 'DPO_COUNTRY', 'DPO_PHONE', 'DPO_EMAIL', 'DPO_WEB',
    'SUPAUTH_NAME', 'SUPAUTH_STREET', 'SUPAUTH_PCODE', 'SUPAUTH_CITY', 'SUPAUTH_COUNTRY',
    'SUPAUTH_PHONE', 'SUPAUTH_EMAIL', 'SUPAUTH_WEB', 'SUPAUTH_PIA_REQUIRED_LIST',
    'CERT_ISSUED_BY', 'CERT_VALID_UNTIL', 'CERT_FP_SHA1', 'CERT_FP_SHA256',
    'DPO_COMM_COL_PRS', 'DPO_COMM_COL_MIS', 'DPO_COMM_COL_CHK', 'DPO_COMM_COL_DEF',
    'DPO_COMMENT', 'DPO_COMMENT_HELPTEXT',
]

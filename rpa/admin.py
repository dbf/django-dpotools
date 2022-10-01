from django.contrib import admin

from .models import Rpa
from .models import ProcessingActivityName
from .models import DataController
from .models import JointController
from .models import DataProtectionOfficer
from .models import InternallyResponsibleDept
from .models import CategoryOfPersonalData
from .models import CategoriesOfPersonalDataOrigin
from .models import PurposeAndLegalBasis
from .models import DataSubject
from .models import TimeLimitForErasure
from .models import CategoryOfRecipients
from .models import TransferToThirdCountry
from .models import AccessGroup
from .models import Transparency
from .models import DataProcessor
from .models import PrivacyImpactAssessment
from .models import TOM
from .models import RPAAnnex

admin.site.register(Rpa)
admin.site.register(ProcessingActivityName)
admin.site.register(DataController)
admin.site.register(JointController)
admin.site.register(DataProtectionOfficer)
admin.site.register(InternallyResponsibleDept)
admin.site.register(CategoryOfPersonalData)
admin.site.register(CategoriesOfPersonalDataOrigin)
admin.site.register(PurposeAndLegalBasis)
admin.site.register(DataSubject)
admin.site.register(TimeLimitForErasure)
admin.site.register(CategoryOfRecipients)
admin.site.register(TransferToThirdCountry)
admin.site.register(AccessGroup)
admin.site.register(Transparency)
admin.site.register(DataProcessor)
admin.site.register(PrivacyImpactAssessment)
admin.site.register(TOM)
admin.site.register(RPAAnnex)

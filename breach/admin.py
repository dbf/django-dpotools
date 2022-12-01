from django.contrib import admin

from .models import Breach
from .models import BreachDataController
from .models import BreachTimeLine
from .models import BreachDescription
from .models import BreachAffectedData
from .models import BreachAffectedSubjects
from .models import BreachConsequences
from .models import BreachMeasures
from .models import BreachCommunication

admin.site.register(Breach)
admin.site.register(BreachDataController)
admin.site.register(BreachTimeLine)
admin.site.register(BreachDescription)
admin.site.register(BreachAffectedData)
admin.site.register(BreachAffectedSubjects)
admin.site.register(BreachConsequences)
admin.site.register(BreachMeasures)
admin.site.register(BreachCommunication)

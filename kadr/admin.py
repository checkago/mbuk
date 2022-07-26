from django.contrib import admin

from kadr.models import *


admin.site.register(EmployeeAddress)
admin.site.register(EmployeeCard)
admin.site.register(CovidCertificate)
admin.site.register(Reason)


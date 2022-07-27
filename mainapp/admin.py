from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from mainapp.models import *


class EmployeeAdmin(ImportExportModelAdmin):
    list_display = ('user', 'last_name', 'first_name', 'middle_name', 'birthday', 'position', 'phone', 'email',
                    'status', 'label')


class PositionAdmin(ImportExportModelAdmin):
    list_display = ('name', 'submission')


class BranchOfficeAdmin(ImportExportModelAdmin):
    list_display = ('organization', 'parent', 'full_name', 'short_name', 'manager', 'email', 'phone', 'address')


"""MAIN"""
admin.site.register(Organization)
admin.site.register(OrganizationBankAccount)
admin.site.register(EmployeeStatus)
admin.site.register(BranchOffice, BranchOfficeAdmin)
admin.site.register(Department)
admin.site.register(Position, PositionAdmin)
admin.site.register(Employee, EmployeeAdmin)
"""KADR"""
admin.site.register(EmployeeAddress)
admin.site.register(EmployeeCard)
admin.site.register(CovidCertificate)
admin.site.register(Reason)
"""CRM"""
admin.site.register(Contragent)
admin.site.register(ContragentBankAccount)
admin.site.register(Contact)
"""DOCUMENTS"""
admin.site.register(IncomingDocument)
admin.site.register(InternalOrderOrganization)
"""GUID"""
admin.site.register(Address)
admin.site.register(Bank)
admin.site.register(Label)

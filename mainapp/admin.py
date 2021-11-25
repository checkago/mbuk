from django.contrib import admin

from mainapp.models import Organization, \
    OrganizationBankAccount, \
    Department, \
    BranchOffice, \
    Position, \
    Employee

admin.site.register(Organization)
admin.site.register(OrganizationBankAccount)
admin.site.register(BranchOffice)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Employee)


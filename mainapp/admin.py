from django.contrib import admin
from import_export import resources

from mainapp.models import Organization, \
    OrganizationBankAccount, \
    Department, \
    BranchOffice, \
    Position, \
    Employee, \
    EmployeeStatus


class EmployeeResource(resources.ModelResource):

    class Meta:
        model = Employee


admin.site.register(Organization)
admin.site.register(OrganizationBankAccount)
admin.site.register(EmployeeStatus)
admin.site.register(BranchOffice)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Employee)


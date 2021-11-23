from django.contrib import admin

from mainapp.models import Organization, BankAccount, Department, BranchOffice, Position, Employee, EmployeeCard

admin.site.register(Organization)
admin.site.register(BankAccount)
admin.site.register(BranchOffice)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Employee)
admin.site.register(EmployeeCard)


from django.contrib import admin
from documents.models import IncomingDocument, InternalOrderOrganization


admin.site.register(IncomingDocument)
admin.site.register(InternalOrderOrganization)
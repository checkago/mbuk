from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from kadr.views import *


urlpatterns = [
    path('employeecard-create/', EmployeeCardCreateView.as_view(), name='employeecard_create'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
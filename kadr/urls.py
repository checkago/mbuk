from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from kadr.views import *


urlpatterns = [
    path('employeescard-list/', EmployeeCardListView.as_view(), name='employees-card-list'),
    path('employeecard-create/', EmployeeCardCreateView.as_view(), name='employeecard-create'),
    path('employees/<int:pk>/', employee_card_view, name='employee_card_view'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
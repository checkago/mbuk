from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from django.contrib.auth.views import LogoutView
from mainapp.views import *


urlpatterns = [
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('', IndexView.as_view(), name='index'),
    path('organizations/', OrganizationListView.as_view(), name='organizations-list'),
    path('employees/', EmployeeListView.as_view(), name='employees-list'),
    path('employee-create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employee-edit/<int:pk>', EmployeeEditView.as_view(), name='employee_edit'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
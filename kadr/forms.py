from django import forms
from kadr.models import EmployeeCard

from django.contrib.auth import get_user_model

User = get_user_model()


class EmployeeCardCreateForm(forms.ModelForm):
    class Meta:
        model = EmployeeCard
        fields = '__all__'


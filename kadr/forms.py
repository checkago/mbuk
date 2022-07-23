from django import forms
from kadr.models import EmployeeCard

from django.contrib.auth import get_user_model

User = get_user_model()


class EmployeeCardCreateForm(forms.ModelForm):

    passport_date_of_issue = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    adopted_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    dismissed_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    digital_work_book = forms.BooleanField(initial=True, required=False, widget=forms.CheckboxInput(attrs={'type': 'checkbox'}))
    paper_work_book = forms.BooleanField(initial=False, required=False, widget=forms.CheckboxInput(attrs={'type': 'checkbox'}))

    class Meta:
        model = EmployeeCard
        fields = '__all__'


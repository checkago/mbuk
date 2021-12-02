from django import forms
from django.contrib.auth import get_user_model
from mainapp.models import Employee

User = get_user_model()


class LoginForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password", "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username).first()

        if not user:
            raise forms.ValidationError(f'Пользователь с логином {username} не найден')

        if not user.check_password(password):
            raise forms.ValidationError(f'Неверный пароль')
        return self.cleaned_data


class RegistrationForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    last_name = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    middle_name = forms.CharField()
    email = forms.EmailField(required=False, widget=forms.EmailInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['birth_date'].label = 'Дата рождения'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтверждение пароля'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['first_name'].label = 'Имя'
        self.fields['middle_name'].label = 'Отчество'
        self.fields['email'].label = 'E-mail'

    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('.')[-1]
        if domain in ['com', 'net', 'org', 'xyz']:
            raise forms.ValidationError(f'Использование почтового ящика в домене .{domain} не разрешена')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Данный почтовый ящик уже зарегистрирован')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Имя {username} занято')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'birth_date', 'first_name', 'last_name', 'email']
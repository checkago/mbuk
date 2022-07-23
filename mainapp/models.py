from django.conf import settings
from django.db import models
from utils import image_upload_function
from guide.models import Bank, Address, Label


class Organization(models.Model):
    full_name = models.CharField(max_length=250, verbose_name='Полное наименование')
    short_name = models.CharField(max_length=250, verbose_name='Краткое наименование')
    logo = models.ImageField(upload_to=image_upload_function, blank=True, verbose_name='Логотип')
    legal_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='legal_address',
                                      verbose_name='Юридический адрес')
    fact_address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, related_name='fact_address',
                                     verbose_name='Почтовый адрес')
    inn = models.CharField(max_length=10, verbose_name='ИНН')
    kpp = models.CharField(max_length=9, verbose_name='КПП')
    okpo = models.CharField(max_length=8, verbose_name='ОКПО')
    ogrn = models.CharField(max_length=13, verbose_name='ОГРН')
    registration_date = models.DateField(verbose_name='Дата регистрации')
    bank_details = models.ForeignKey('OrganizationBankAccount', on_delete=models.CASCADE, verbose_name='Баковские реквизиты')
    primary = models.BooleanField(default=False, verbose_name='Основная')

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.short_name


class OrganizationBankAccount(models.Model):
    name = models.CharField(max_length=150, verbose_name='Рабочее название')
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, verbose_name='Банк')

    RUB = 'Рубль'
    EUR = 'Евро'
    USD = 'Доллар'

    CURRENCY = (
        (RUB, 'Рубль'),
        (EUR, 'Евро'),
        (USD, 'Доллар')
    )
    payment_account = models.CharField(max_length=20, verbose_name='Расчетный счет')
    account_currency = models.CharField(max_length=10, blank=True, null=True, choices=CURRENCY, default=RUB,
                                        verbose_name='Валюта счета')

    class Meta:
        verbose_name = 'Банковский Счет'
        verbose_name_plural = 'Банковские счета организации'

    def __str__(self):
        return self.name


class BranchOffice(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Организация')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='childs',
                               null=True, blank=True, verbose_name='Подчиняется')
    full_name = models.CharField(max_length=250, verbose_name='Полное наименование')
    short_name = models.CharField(max_length=250, verbose_name='Краткое наименование')
    manager = models.ForeignKey('Employee', blank=True, on_delete=models.SET_NULL,
                                null=True, verbose_name='Руководитель подразделения')
    email = models.EmailField(verbose_name='Почта')
    phone = models.CharField(max_length=18, verbose_name='Номер телефона')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name='Адрес')
    departments = models.ManyToManyField('Department', blank=True, verbose_name='Отделы')

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы/Подразделения'

    def __str__(self):
        return f"{self.short_name} - {self.organization}"


class Department(models.Model):
    parent_branch = models.ForeignKey(BranchOffice, on_delete=models.CASCADE, verbose_name='Входит в состав')
    name = models.CharField(max_length=250, verbose_name='Наименование')
    manager = models.ForeignKey('Employee', blank=True, on_delete=models.SET_NULL, null=True, related_name='manager',
                                verbose_name='Руководитель')
    employees = models.ManyToManyField('Employee', blank=True, related_name='employees', verbose_name='Сотрудники')
    email = models.EmailField(blank=True, verbose_name='Почта')
    phone = models.CharField(max_length=18, blank=True, verbose_name='Номер телефона')

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return f"{self.name} - {self.parent_branch}"


class Position(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    submission = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='childs',
                               null=True, blank=True, verbose_name='Подчиняется')

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return self.name


class Employee(models.Model):
    # Связь с пользователем
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    middle_name = models.CharField(max_length=150, blank=True, verbose_name='Отчество')
    birthday = models.DateField(null=True, verbose_name='Дата рождения')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, verbose_name='Должность')
    salary = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Оклад')

    @property
    def label(self):
        return Label.objects.order_by("?").first()


    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f"{self.last_name} {self.first_name}  - пользователь({self.user})"



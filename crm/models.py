from django.db import models
from utils import file_upload_function, image_upload_function
from mainapp.models import Organization
from guide.models import Address, Bank


class Contragent(models.Model):
    organization = models.ForeignKey(Organization, null=True, on_delete=models.SET_NULL, verbose_name='Организация')
    name = models.CharField(max_length=250, blank=True, verbose_name='Полное наименование')
    short_name = models.CharField(max_length=150, verbose_name='Рабочее наименование')
    logo = models.ImageField(upload_to=image_upload_function, blank=True, verbose_name='Логотип')
    legal_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='contragent_legal_address', verbose_name='Юридический адрес')
    fact_address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, related_name='contragent_fact_address', verbose_name='Почтовый адрес')
    inn = models.CharField(max_length=10, verbose_name='ИНН')
    kpp = models.CharField(max_length=9, verbose_name='КПП')
    okpo = models.CharField(max_length=8, blank=True, verbose_name='ОКПО')
    bank_details = models.ForeignKey('ContragentBankAccount', blank=True, on_delete=models.CASCADE, null=True,
                                     verbose_name='Баковские реквизиты')

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'

    def __str__(self):
        return self.short_name


class ContragentBankAccount(models.Model):
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
        verbose_name = 'Банковский счет контрагента'
        verbose_name_plural = 'Банковские счета контрагентов'

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название в списке')
    company = models.ForeignKey(Contragent, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Контрагент')
    last_name = models.CharField(max_length=100, blank=True, verbose_name='Фамилия')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    middle_name = models.CharField(max_length=100, verbose_name='Отчество')
    image = models.ImageField(upload_to=image_upload_function, blank=True, verbose_name='Фото')
    phone = models.CharField(max_length=18, verbose_name='Номер телефона')
    email = models.EmailField(blank=True, verbose_name='Email')
    whatsapp = models.BooleanField(default=True, verbose_name='Есть whatsapp')
    viber = models.BooleanField(default=False, verbose_name='Есть viber')
    telegram = models.BooleanField(default=False, verbose_name='Есть telegram')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return self.name

from django.db import models


class Bank(models.Model):
    bank_name = models.CharField(max_length=250, verbose_name='Наименование банка')
    bic_number = models.CharField(max_length=9, verbose_name='БИК Банка')
    correspondent_account = models.CharField(max_length=20, verbose_name='Кор. счет')

    class Meta:
        verbose_name = 'Банк'
        verbose_name_plural = 'Банки'

    def __str__(self):
        return self.bank_name


class Address(models.Model):
    region = models.CharField(max_length=150, verbose_name='Область/Край')
    district = models.CharField(max_length=150, blank=True, verbose_name='Район')
    city = models.CharField(max_length=150, verbose_name='Населенный пункт')
    neighborhood = models.CharField(max_length=150, blank=True, verbose_name='Микрорайон')
    street = models.CharField(max_length=200, verbose_name='Улица')
    building = models.CharField(max_length=4, verbose_name='Дом/Строение')
    apartment = models.CharField(max_length=3, blank=True, verbose_name='Квартира')

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return f"{self.city}, {self.neighborhood}, {self.street}, {self.building}"


class Label(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    color = models.CharField(max_length=20, verbose_name='Цвет')

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    def __str__(self):
        return self.name

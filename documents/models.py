from django.db import models
from utils import file_upload_function
from crm.models import Contragent
from mainapp.models import Organization, Position


class IncomingDocument(models.Model):

    ORDER = 'Приказ'
    LETTER = 'Письмо'
    REQUIREMENT = 'Требование'

    DOCUMENT_TYPES = (
        (ORDER, 'Приказ'),
        (LETTER, 'Письмо'),
        (REQUIREMENT, 'Требование')
    )

    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, default=ORDER)
    contragent = models.ForeignKey(Contragent, on_delete=models.SET_NULL, null=True, verbose_name='Организация')
    number = models.CharField(max_length=50, blank=True, verbose_name='Номер')
    date = models.DateField(verbose_name='Дата')
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    scan_image = models.FileField(upload_to=file_upload_function, verbose_name='Скан документа')

    class Meta:
        verbose_name = 'Входящий документ'
        verbose_name_plural = 'Входящие документы'

    def __str__(self):
        return f"{self.document_type} №{self.number} от {self.date} - {self.contragent}"


class InternalOrderOrganization(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Организация')
    number = models.CharField(max_length=50, verbose_name='Номер')
    date = models.DateField(verbose_name='Дата')
    base_order = models.ForeignKey(IncomingDocument, blank=True, on_delete=models.SET_NULL, null=True,
                                   verbose_name='Основание')
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    text = models.TextField(blank=True, verbose_name='Текст')
    scan_image = models.FileField(upload_to=file_upload_function, verbose_name='Скан документа')

    class Meta:
        verbose_name = 'Приказ по организации'
        verbose_name_plural = 'Приказы по организации'

    def __str__(self):
        return f"№{self.number} от {self.date} - {self.organization}"


class ApplicationForEmployment(models.Model):
    interval_number = models.CharField(max_length=10, blank=True, verbose_name='Внутренний номер')
    date = models.DateField(verbose_name='Дата')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, verbose_name='Должность')
    application_scan = models.FileField(upload_to=file_upload_function,)

    class Meta:
        verbose_name = 'Заявление на работу'
        verbose_name_plural = 'Заявления на работу'

    def __str__(self):
        return f"№{self.interval_number} от {self.date} на должность {self.position}"





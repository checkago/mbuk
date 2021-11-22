from datetime import datetime
from django.conf import settings
from django.db import models
from utils import upload_function


class Organization(models.Model):
    full_name = models.CharField(max_length=250, verbose_name='Полное наименование')
    short_name = models.CharField(max_length=250, verbose_name='Краткое наименование')
    logo = models.ImageField(upload_to=upload_function, blank=True, verbose_name='Логотип')
    legal_address = models.ForeignKey('Address', on_delete=models.CASCADE, verbose_name='Юридический адрес')
    fact_address = models.ForeignKey('Address', on_delete=models.CASCADE, verbose_name='Фактический адрес')
    inn = models.CharField(max_length=10, verbose_name='ИНН')
    kpp = models.CharField(max_length=9, verbose_name='КПП')
    okpo = models.CharField(max_length=8, verbose_name='ОКПО')
    ogrn = models.CharField(max_length=13, verbose_name='ОГРН')
    registration_date = models.DateField(verbose_name='Дата регистрации')
    bank_details = models.ForeignKey('BankDetails', on_delete=models.CASCADE, verbose_name='Баковские реквизиты')

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class BankDetails(models.Model):

    RUB = 'Рубль'
    EUR = 'Евро'
    USD = 'Доллар'

    CURRENCY = (
        (RUB, 'Рубль'),
        (EUR, 'Евро'),
        (USD, 'Доллар')
    )
    bank_name = models.CharField(max_length=250, verbose_name='Наименование банка')
    bic_number = models.CharField(max_length=9, verbose_name='БИК Банка')
    payment_account = models.CharField(max_length=20, verbose_name='Расчетный счет')
    correspondent_account = models.CharField(max_length=20, verbose_name='Кор. счет')
    account_currency = models.CharField(max_length=10, blank=True, null=True, choices=CURRENCY, default=RUB,
                                        verbose_name='Валюта счета')


class BranchOffice(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Организация')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='childs',
                               null=True, blank=True, verbose_name='Подчиняется')
    full_name = models.CharField(max_length=250, verbose_name='Полное наименование')
    short_name = models.CharField(max_length=250, verbose_name='Краткое наименование')
    manager = models.ForeignKey('Employee', on_delete=models.SET_NULL,
                                null=True, verbose_name='Руководитель подразделения')
    email = models.EmailField(verbose_name='Почта')
    phone = models.CharField(max_length=18, verbose_name='Номер телефона')
    address = models.ForeignKey('Address', on_delete=models.CASCADE, verbose_name='Адрес')
    departments = models.ManyToManyField('Department', blank=True, null=True, verbose_name='Отделы')

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы/Подразделения'


class Department(models.Model):
    parent_branch = models.ForeignKey(BranchOffice, on_delete=models.CASCADE, )
    name = models.CharField(max_length=250, verbose_name='Наименование')
    manager = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, verbose_name='Руководитель')
    employees = models.ManyToManyField('Employee', verbose_name='Сотрудники')
    email = models.EmailField(blank=True, verbose_name='Почта')
    phone = models.CharField(max_length=18, blank=True, verbose_name='Номер телефона')

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'


class Position(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    submission = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='childs',
                               null=True, blank=True, verbose_name='Подчиняется')

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class Employee(models.Model):
    # Связь с пользователем
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')

    # Персональные данные
    MALE = 'Мужской'
    FEMALE = 'Женский'

    NOT_MARRIED = 'Не женат/Не замужем'
    MARRIED = 'Женат/Замужем'
    WIDOW = 'Вдовец/вдова'
    DIVORCED = 'Разведен/Разведена'

    SEX_CHOICE = (
        (MALE, 'Мужской'),
        (FEMALE, 'Женский')
    )
    MARRIED_STATUS_CHOICE = (
        (NOT_MARRIED, 'Не женат/Не замужем'),
        (MARRIED, 'Женат/Замужем'),
        (WIDOW, 'Вдовец/вдова'),
        (DIVORCED, 'Разведен/Разведена')
    )
    """Имя и Фамилия беруться из модели User"""
    i_middle_name = models.CharField(max_length=150, verbose_name='Отчество')
    r_first_name = models.CharField(max_length=150, verbose_name='Имя')
    r_last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    r_middle_name = models.CharField(max_length=150, verbose_name='Отчество')
    d_first_name = models.CharField(max_length=150, verbose_name='Имя')
    d_last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    d_middle_name = models.CharField(max_length=150, verbose_name='Отчество')
    image = models.ImageField(upload_to=upload_function, blank=True, verbose_name='Фото')

    # ПАСПОРТНЫЕ ДАННЫЕ
    passport_serial = models.CharField(max_length=4, verbose_name='Серия паспорта')
    passport_number = models.CharField(max_length=6, verbose_name='Номер паспорта')
    passport_issuing = models.CharField(max_length=250, verbose_name='Кем выдан')
    passport_date_of_issue = models.DateField(verbose_name='Дата выдачи')
    issuing_office_number = models.CharField(max_length=7, verbose_name='Код подразделения')
    birthday = models.DateField(verbose_name='Дата рождения')
    sex = models.CharField(max_length=10, blank=True, null=True, choices=SEX_CHOICE, verbose_name='Пол')
    marital_status = models.CharField(max_length=10, blank=True, null=True, choices=MARRIED_STATUS_CHOICE,
                                      verbose_name='Семейное положение')
    main_address = models.ForeignKey('Address', blank=True, on_delete=models.CASCADE,
                                     verbose_name='Адрес постоянной регистрации')
    place_of_stay_address = models.ForeignKey('Address', blank=True, on_delete=models.CASCADE,
                                              verbose_name='Адрес временной регистрации')

    # СТАЖ и ПФР
    experience_before = models.IntegerField(max_length=2, verbose_name='Предыдущий стаж')
    digital_work_book = models.BooleanField(default=False, verbose_name='"Электронная')
    paper_work_book = models.BooleanField(default=False, verbose_name='Бумажная')
    paper_work_book_image = models.ImageField(upload_to=upload_function, blank=True,
                                              verbose_name='Скан бумажной трудовой')

    # ДОКУМЕНТЫ
    # Заявление о приеме на работу
    job_application = models.ForeignKey('Application', on_delete=models.SET_NULL, blank=True, null=True,
                                        verbose_name='Заявление о приеме на работу')
    # Приказ о приеме на работу
    adopted_order = models.ForeignKey('Order', on_delete=models.SET_NULL, blank=True, null=True,
                                      verbose_name='Прием на работу')
    # Трудовой договор
    employment_contract = models.ForeignKey('EmploymentContract', on_delete=models.SET_NULL, blank=True, null=True,
                                            verbose_name='Прием на работу')


    @property
    def experience_current(self):
        return int((datetime.now().date() - self.adopted_date).days / 365.25)

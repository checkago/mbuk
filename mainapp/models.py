from datetime import datetime
from django.conf import settings
from django.db import models
from utils import upload_function
from guide.models import Bank, Address


class Organization(models.Model):
    full_name = models.CharField(max_length=250, verbose_name='Полное наименование')
    short_name = models.CharField(max_length=250, verbose_name='Краткое наименование')
    logo = models.ImageField(upload_to=upload_function, blank=True, verbose_name='Логотип')
    legal_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='legal_address', verbose_name='Юридический адрес')
    fact_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='fact_address', verbose_name='Фактический адрес')
    inn = models.CharField(max_length=10, verbose_name='ИНН')
    kpp = models.CharField(max_length=9, verbose_name='КПП')
    okpo = models.CharField(max_length=8, verbose_name='ОКПО')
    ogrn = models.CharField(max_length=13, verbose_name='ОГРН')
    registration_date = models.DateField(verbose_name='Дата регистрации')
    bank_details = models.ForeignKey('BankAccount', on_delete=models.CASCADE, verbose_name='Баковские реквизиты')

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.short_name


class BankAccount(models.Model):
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
        verbose_name_plural = 'Банковские счета'

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
    phone = models.CharField(max_length=18, verbose_name='Номер телефона')
    whatsapp = models.BooleanField(default=True, verbose_name='Есть whatsapp')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, verbose_name='Должность')
    branch_office = models.ForeignKey(BranchOffice, on_delete=models.SET_NULL, null=True, verbose_name='Филиал')
    salary = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name='Оклад')
    card = models.OneToOneField('EmployeeCard', blank=True, null=True, related_name='card', on_delete=models.SET_NULL,
                                verbose_name='Карточка сотрудника')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Список Сотрудников'

    def __str__(self):
        return f"{self.last_name} {self.first_name} - пользователь({self.user})"


class EmployeeCard(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Сотрудник')
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
    r_first_name = models.CharField(max_length=150, verbose_name='Имя "Кого?"')
    r_last_name = models.CharField(max_length=150, verbose_name='Фамилия "Кого?"')
    r_middle_name = models.CharField(max_length=150, verbose_name='Отчество "Кого?"')
    d_first_name = models.CharField(max_length=150, verbose_name='Имя "Кому?"')
    d_last_name = models.CharField(max_length=150, verbose_name='Фамилия "Кому?"')
    d_middle_name = models.CharField(max_length=150, verbose_name='Отчество "Кому?"')
    image = models.ImageField(upload_to=upload_function, blank=True, verbose_name='Фото')

    # ПАСПОРТНЫЕ ДАННЫЕ
    passport_serial = models.CharField(max_length=4, verbose_name='Серия паспорта')
    passport_number = models.CharField(max_length=6, verbose_name='Номер паспорта')
    passport_issuing = models.CharField(max_length=250, verbose_name='Кем выдан')
    passport_date_of_issue = models.DateField(verbose_name='Дата выдачи')
    issuing_office_number = models.CharField(max_length=7, verbose_name='Код подразделения')
    birthday = models.DateField(verbose_name='Дата рождения')
    sex = models.CharField(max_length=10, blank=True, null=True, choices=SEX_CHOICE, verbose_name='Пол')
    marital_status = models.CharField(max_length=25, blank=True, null=True, choices=MARRIED_STATUS_CHOICE,
                                      verbose_name='Семейное положение')
    main_address = models.ForeignKey(Address, blank=True, on_delete=models.CASCADE,
                                     verbose_name='Адрес постоянной регистрации')
    place_of_stay_address = models.ForeignKey(Address, blank=True, on_delete=models.CASCADE,
                                              related_name='place_of_stay_address',
                                              verbose_name='Адрес временной регистрации')

    # СВЕДЕНИЯ о РАБОТЕ и СТАЖ
    adopted_date = models.DateField(auto_now_add=True, blank=True, verbose_name='Принят')
    dismissed_date = models.DateField(blank=True, verbose_name='Дата увольнения')
    experience_before = models.IntegerField(verbose_name='Предыдущий стаж')
    digital_work_book = models.BooleanField(default=False, verbose_name='"Электронная')
    paper_work_book = models.BooleanField(default=False, verbose_name='Бумажная')
    paper_work_book_image = models.ImageField(upload_to=upload_function, blank=True,
                                              verbose_name='Скан бумажной трудовой')

    # ДОКУМЕНТЫ
    # Заявление о приеме на работу
    # job_application = models.ForeignKey('Application', on_delete=models.SET_NULL, blank=True, null=True,
    #                                     verbose_name='Заявление о приеме на работу')
    # Приказ о приеме на работу
    # adopted_order = models.ForeignKey('Order', on_delete=models.SET_NULL, blank=True, null=True,
    #                                   verbose_name='Прием на работу')
    # Трудовой договор
    # employment_contract = models.ForeignKey('EmploymentContract', on_delete=models.SET_NULL, blank=True, null=True,
    #                                         verbose_name='Прием на работу')

    @property
    def experience_current(self):
        return int((datetime.now().date() - self.adopted_date).days / 365.25)

    class Meta:
        verbose_name = 'Карточка сотрудника'
        verbose_name_plural = 'Личные карточки сотрудников'

    def __str__(self):
        return f"Карточка сотрудника {self.employee}"

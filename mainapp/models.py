from django.conf import settings
from django.db import models
from datetime import datetime
from utils import image_upload_function, file_upload_function


"""MAIN"""


class EmployeeStatus(models.Model):
    name = models.CharField(max_length=150, verbose_name='Нименование')
    color = models.ForeignKey('Label', max_length=50, blank=True, on_delete=models.CASCADE, verbose_name='Цвет')

    class Meta:
        verbose_name = 'Статус сотрудника'
        verbose_name_plural = 'Статусы сотрудников'

    def __str__(self):
        return self.name


class Organization(models.Model):
    full_name = models.CharField(max_length=250, verbose_name='Полное наименование')
    short_name = models.CharField(max_length=250, verbose_name='Краткое наименование')
    director = models.ForeignKey('Employee', blank=True, on_delete=models.SET_NULL, null=True, verbose_name='Директор')
    logo = models.ImageField(upload_to=image_upload_function, blank=True, verbose_name='Логотип')
    legal_address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='legal_address',
                                      verbose_name='Юридический адрес')
    fact_address = models.ForeignKey('Address', on_delete=models.CASCADE, blank=True, related_name='fact_address',
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
    bank = models.ForeignKey('Bank', on_delete=models.CASCADE, verbose_name='Банк')

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
    address = models.ForeignKey('Address', on_delete=models.CASCADE, verbose_name='Адрес')
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
    phone = models.CharField(max_length=18, blank=True, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Почта')
    status = models.ForeignKey(EmployeeStatus, on_delete=models.SET_NULL, null=True, verbose_name='Рабочий статус')

    @property
    def label(self):
        return Label.objects.order_by("?").first()


    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f"{self.last_name} {self.first_name}  - пользователь({self.user})"



"""KADR"""


class EmployeeAddress(models.Model):
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


class EmployeeCard(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name="employee_card",
                                    verbose_name="Сотрудник")
    branch_office = models.ForeignKey(BranchOffice, blank=True, on_delete=models.SET_NULL, null=True,
                                      verbose_name='Филиал')
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
    image = models.ImageField(upload_to=image_upload_function, blank=True, verbose_name='Фото')

    # ПАСПОРТНЫЕ ДАННЫЕ
    passport_serial = models.CharField(max_length=4, verbose_name='Серия паспорта')
    passport_number = models.CharField(max_length=6, verbose_name='Номер паспорта')
    passport_issuing = models.CharField(max_length=250, verbose_name='Кем выдан')
    passport_date_of_issue = models.DateField(verbose_name='Дата выдачи')
    issuing_office_number = models.CharField(max_length=7, verbose_name='Код подразделения')
    sex = models.CharField(max_length=10, blank=True, null=True, choices=SEX_CHOICE, verbose_name='Пол')
    marital_status = models.CharField(max_length=25, blank=True, null=True, choices=MARRIED_STATUS_CHOICE,
                                      verbose_name='Семейное положение')
    children = models.IntegerField(blank=True, null=True, verbose_name='Несовершеннолетние дети')
    main_address = models.CharField(max_length=150, blank=True, verbose_name='Адрес регистрации')
    inn = models.CharField(max_length=12, blank=True, verbose_name='ИНН')
    snils = models.CharField(max_length=11, blank=True, verbose_name='СНИЛС')
    passport_copy = models.FileField(upload_to=file_upload_function, blank=True, verbose_name='Копия паспорта')

    # СВЕДЕНИЯ о РАБОТЕ и СТАЖ
    adopted_date = models.DateField(blank=True, verbose_name='Принят')
    dismissed_date = models.DateField(blank=True, verbose_name='Дата увольнения')
    bib_experience_before = models.FloatField(default=0, blank=True, verbose_name='Предыдущий стаж библиотечный')
    experience_before = models.FloatField(default=0, blank=True, verbose_name='Предыдущий стаж полный')
    digital_work_book = models.BooleanField(default=False, blank=True, verbose_name='"Электронная')
    paper_work_book = models.BooleanField(default=False, blank=True, verbose_name='Бумажная')
    paper_work_book_image = models.FileField(upload_to=file_upload_function, blank=True,
                                             verbose_name='Скан бумажной трудовой')

    # ДОКУМЕНТЫ
    # Заявление о приеме на работу
    appliccaton_for_employment = models.ForeignKey('ApplicationForEmployment', on_delete=models.SET_NULL,
                                                   blank=True, null=True, verbose_name='Заявление о приеме на работу')
    # Заявление о переводе
    appliccaton_for_transfer = models.ForeignKey('ApplicationForPositionTransfer', on_delete=models.SET_NULL,
                                                   blank=True, null=True, verbose_name='Заявление о приеме на работу')
    # Приказ о приеме на работу
    order_for_employment = models.ForeignKey('OrderForEmployment', on_delete=models.SET_NULL, blank=True, null=True,
                                             verbose_name='Приказ о приеме на работу')
    # Трудовой договор
    work_contract = models.ForeignKey('WorkContract', on_delete=models.SET_NULL, blank=True, null=True,
                                      verbose_name='Трудовой договор')
    # Должностные инструкции
    position_instruction = models.ForeignKey('PositionInstruction', on_delete=models.SET_NULL, blank=True, null=True,
                                             verbose_name='Должностные инструкции')
    #Соглашение о персональных данных
    covid_certificate = models.FileField(blank=True, verbose_name='Сертификат вакцинированного')

    appliccaton_for_dissmiss = models.ForeignKey('ApplicationForDismissal', on_delete=models.SET_NULL,
                                                   blank=True, null=True, verbose_name='Заявление на увольнение')

    @property
    def experience_current(self):
        experience_current_d = float((datetime.now().date() - self.adopted_date).days / 365.25)
        a = experience_current_d % 1
        a_float = float(a * 12)
        a_round = round(a_float, 0) - 1
        a_int = int(a_round)
        b = experience_current_d // 1
        b_int = int(b)
        return f"{b_int} г/л., {a_int} мес."

    @property
    def experience_current_int(self):
        experience_current = float((datetime.now().date() - self.adopted_date).days / 365.25)
        return experience_current

    @property
    def age(self):
        age = int((datetime.now().date() - self.employee.birthday).days / 365.25)
        return age

    @property
    def bib_experience_before_all(self):
        bib_experience_before_all_d = float(self.experience_current_int + (self.bib_experience_before / 12))
        a = bib_experience_before_all_d % 1
        a_float = float(a * 12)
        a_round = round(a_float, 0) - 1
        a_int = int(a_round)
        b = bib_experience_before_all_d // 1
        b_int = int(b)
        return f"{b_int} г/л., {a_int} мес."

    @property
    def bib_experience_before_all_int(self):
        bib_experience_before_all = int(self.experience_current_int + self.bib_experience_before)
        return bib_experience_before_all

    @property
    def experience_full(self):
        experience_full_d = float(self.experience_current_int + (self.experience_before / 12))
        a = experience_full_d % 1
        a_float = float(a * 12)
        a_round = round(a_float, 0) - 1
        a_int = int(a_round)
        b = experience_full_d // 1
        b_int = int(b)
        return f"{b_int} г/л., {a_int} мес."

    @property
    def experience_full_int(self):
        experience_full = float(self.experience_current_int + self.experience_before)
        return experience_full

    @property
    def label(self):
        return Label.objects.order_by("?").first()

    class Meta:
        verbose_name = 'Карточка сотрудника'
        verbose_name_plural = 'Карточки сотрудников'

    def __str__(self):
        return f"Карточка {self.r_last_name} {self.r_first_name}"


class ApplicationForEmployment(models.Model):
    internal_number = models.CharField(max_length=10, blank=True, verbose_name='Внутренний номер')
    date = models.DateField(verbose_name='Дата')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, verbose_name='Должность')
    application_scan = models.FileField(upload_to=file_upload_function,)

    class Meta:
        verbose_name = 'Заявление на прием на работу'
        verbose_name_plural = 'Заявления на прием на работу'

    def __str__(self):
        return f"прием №{self.internal_number} от {self.date} на должность {self.position}"


class ApplicationForTransfer(models.Model):
    internal_number = models.CharField(max_length=10, blank=True, verbose_name='Внутренний номер')
    date = models.DateField(verbose_name='Дата')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, verbose_name='На должность')
    application_scan = models.FileField(upload_to=file_upload_function,)

    class Meta:
        verbose_name = 'Заявление на перевод'
        verbose_name_plural = 'Заявления на перевод'

    def __str__(self):
        return f"увольнение №{self.internal_number} от {self.date} с должности {self.position}"


class ApplicationForDismissal(models.Model):
    internal_number = models.CharField(max_length=10, blank=True, verbose_name='Внутренний номер')
    date = models.DateField(verbose_name='Дата')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, verbose_name='Должность')
    reason = models.ForeignKey('Reason', blank=True, on_delete=models.SET_NULL, null=True, verbose_name='Причина')
    application_scan = models.FileField(upload_to=file_upload_function,)

    class Meta:
        verbose_name = 'Заявление на увольнение'
        verbose_name_plural = 'Заявления на увольнение'

    def __str__(self):
        return f"увольнение №{self.internal_number} от {self.date} с должности {self.position}"


class ApplicationForPositionTransfer(models.Model):
    internal_number = models.CharField(max_length=10, blank=True, verbose_name='Внутренний номер')
    date = models.DateField(verbose_name='Дата')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, verbose_name='Должность')
    reason = models.ForeignKey('Reason', blank=True, on_delete=models.SET_NULL, null=True, verbose_name='Причина')
    application_scan = models.FileField(upload_to=file_upload_function, verbose_name='Скан заявления')

    class Meta:
        verbose_name = 'Заявление на перевод'
        verbose_name_plural = 'Заявления на перевод'

    def __str__(self):
        return f"перевод №{self.internal_number} от {self.date} на должность {self.position}"


class OrderForEmployment(models.Model):
    number = models.CharField(max_length=10, verbose_name='Номер')
    date = models.DateField(verbose_name='Дата')
    employee = models.ForeignKey(Employee, blank=True, on_delete=models.SET_NULL, null=True, verbose_name='Сотрудник')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, verbose_name='Должность')
    scan_file = models.FileField(upload_to=file_upload_function, verbose_name='Скан приказа')

    class Meta:
        verbose_name = 'Приказ о приеме на работу'
        verbose_name_plural = 'Приказы о приеме на работу'

    def __str__(self):
        return f"№{self.number} от {self.date} на должность {self.position}"


class WorkContract(models.Model):
    number = models.CharField(max_length=10, verbose_name='Номер')
    date = models.DateField(verbose_name='Дата')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Организация')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Сотрудник')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, verbose_name='Должность')

    class Meta:
        verbose_name = 'Трудовой договор'
        verbose_name_plural = 'Трудовые договоры'

    def __str__(self):
        return f"{self.number}/{self.date} ({self.employee})"


class PersonalDataAgreement(models.Model):
    employee = models.ForeignKey(EmployeeCard, on_delete=models.CASCADE, verbose_name='Соглашение о персоналных данных')
    number = models.CharField(max_length=10, verbose_name='Номер')
    date = models.DateField(verbose_name='Дата')
    agreement_file = models.FileField(upload_to=file_upload_function, verbose_name='Скан документа')

    class Meta:
        verbose_name = 'Соглашение об обработке персоналных данных'
        verbose_name_plural = 'Соглашения об обработке персональных данных'

    def __str__(self):
        return self.employee


class PositionInstruction(models.Model):
    date = models.DateField(verbose_name='Дата')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, verbose_name='Должность')
    file = models.FileField(upload_to=file_upload_function, verbose_name='Файл инструкций')

    class Meta:
        verbose_name = 'Должностная инструкция'
        verbose_name_plural = 'Должностные инструкции'

    def __str__(self):
        return f"{self.date} ({self.position})"


class CovidCertificate(models.Model):
    employee = models.ForeignKey(EmployeeCard, on_delete=models.CASCADE, verbose_name='Сертифика о вакцинации')
    number = models.CharField(max_length=10, verbose_name='Номер')
    date = models.DateField(verbose_name='Дата')
    certificate_file = models.FileField(upload_to=file_upload_function, verbose_name='Скан документа')

    class Meta:
        verbose_name = 'Сертификат о вакцинации'
        verbose_name_plural = 'Сертификаты вакцинированных'

    def __str__(self):
        return self.employee


""" СПРАВОЧНИКИ """


class Reason(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    article_of_law = models.CharField(max_length=250, blank=True, verbose_name='Статья ТК')

    class Meta:
        verbose_name = 'Причина увольнения'
        verbose_name_plural = 'Причины увольнения'

    def __str__(self):
        return self.name


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


"""DOCUMENTS"""


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
    contragent = models.ForeignKey('Contragent', on_delete=models.SET_NULL, null=True, verbose_name='Организация')
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


"""CRM"""

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
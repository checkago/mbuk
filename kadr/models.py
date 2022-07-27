from django.db import models
from datetime import datetime
from utils import image_upload_function, file_upload_function
from mainapp.models import Employee, Position, Organization, BranchOffice
from guide.models import Label


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
    main_address = models.ForeignKey(EmployeeAddress, blank=True, on_delete=models.SET_NULL, null=True,
                                     related_name='employee_main_address', verbose_name='Адрес регистрации')
    inn = models.CharField(max_length=10, blank=True, verbose_name='ИНН')
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
        a_round = round(a_float, 0)
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
        a_round = round(a_float, 0)
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
        a_round = round(a_float, 0)
        a_int = int(a_round)
        b = experience_full_d // 1
        b_int = int(b)
        return f"{b_int} г/л., {a_int} мес."
        return experience_full


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





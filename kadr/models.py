from django.db import models
from utils import image_upload_function, file_upload_function
from mainapp.models import Employee


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
    birthday = models.DateField(verbose_name='Дата рождения')
    sex = models.CharField(max_length=10, blank=True, null=True, choices=SEX_CHOICE, verbose_name='Пол')
    marital_status = models.CharField(max_length=25, blank=True, null=True, choices=MARRIED_STATUS_CHOICE,
                                      verbose_name='Семейное положение')
    main_address = models.ForeignKey(EmployeeAddress, blank=True, on_delete=models.CASCADE,
                                     related_name='employee_main_address', verbose_name='Адрес постоянной регистрации')
    place_of_stay_address = models.ForeignKey(EmployeeAddress, blank=True, null=True, on_delete=models.CASCADE,
                                              related_name='employee_place_of_stay_address',
                                              verbose_name='Адрес временной регистрации')

    # СВЕДЕНИЯ о РАБОТЕ и СТАЖ
    adopted_date = models.DateField(auto_now_add=True, blank=True, verbose_name='Принят')
    dismissed_date = models.DateField(blank=True, null=True, verbose_name='Дата увольнения')
    experience_before = models.IntegerField(verbose_name='Предыдущий стаж')
    digital_work_book = models.BooleanField(default=False, verbose_name='"Электронная')
    paper_work_book = models.BooleanField(default=False, verbose_name='Бумажная')
    paper_work_book_image = models.FileField(upload_to=file_upload_function, blank=True,
                                              verbose_name='Скан бумажной трудовой')

    # ДОКУМЕНТЫ
    # Заявление о приеме на работу
    #job_application = models.ForeignKey('Application', on_delete=models.SET_NULL, blank=True, null=True,
                                        #verbose_name='Заявление о приеме на работу')
    # Приказ о приеме на работу
    #adopted_order = models.ForeignKey('Order', on_delete=models.SET_NULL, blank=True, null=True,
                                      #verbose_name='Прием на работу')
    # Трудовой договор
    #employment_contract = models.ForeignKey('EmploymentContract', on_delete=models.SET_NULL, blank=True, null=True,
                                            #verbose_name='Прием на работу')

    @property
    def experience_current(self):
        return int((datetime.now().date() - self.adopted_date).days / 365.25)

    class Meta:
        verbose_name = 'Карточка сотрудника'
        verbose_name_plural = 'Карточки сотрудников'

    def __str__(self):
        return f"Карточка {self.r_last_name} {self.r_first_name}"


from django.db import models


class EmployeeCard(models.Model):
    employee = models.OneToOneField(Employee, related_name="card", verbose_name="Сотрудник")
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

    # СВЕДЕНИЯ о РАБОТЕ и СТАЖ
    adopted_date = models.DateField(auto_now_add=True, blank=True, verbose_name='Принят')
    dismissed_date = models.DateField(blank=True, verbose_name='Дата увольнения')
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

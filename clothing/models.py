from django.db import models

DIMENSIONS = [
    (1, '39/1'),
    (2, '39/2'),
]

SHOES_DIMENSIONS = [
    (1, '37'),
    (2, '38'),
]

SEX = [
    (1, 'Мужской'),
    (2, 'Женский'),
]

EMPLOYEE_KIND = [
    (1, 'Курсант'),
    (2, 'Офицер'),
    (1, 'Гражданский'),
]


class Subdivision(models.Model):
    subdivision_name = models.CharField(verbose_name="Подразделение", max_length=255)
    subdivision_short_name = models.CharField(
        verbose_name="Короткое название подразделения (только заглавные английские буквы)", max_length=255)
    created_at = models.DateTimeField(verbose_name="Дата и время создания", auto_created=True, blank=True, null=True)
    last_modified = models.DateTimeField(verbose_name="Дата и время последнего изменения", auto_now=True, blank=True,
                                         null=True)

    def __str__(self):
        return self.subdivision_name

    class Meta:
        ordering = ('subdivision_name',)
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'


class Position(models.Model):
    position = models.CharField(verbose_name="Должность", max_length=255)
    created_at = models.DateTimeField(verbose_name="Дата и время создания", auto_created=True, blank=True, null=True)
    last_modified = models.DateTimeField(verbose_name="Дата и время последнего изменения", auto_now=True, blank=True,
                                         null=True)

    def __str__(self):
        return self.position

    class Meta:
        ordering = ('position',)
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class Rank(models.Model):
    rank = models.CharField(verbose_name="Звание", max_length=50)
    created_at = models.DateTimeField(verbose_name="Дата и время создания", auto_created=True, blank=True, null=True)
    last_modified = models.DateTimeField(verbose_name="Дата и время последнего изменения", auto_now=True, blank=True,
                                         null=True)

    def __str__(self):
        return self.rank

    class Meta:
        ordering = ('id',)
        verbose_name = 'Звание'
        verbose_name_plural = 'Звания'


class Clothes(models.Model):
    clothes_title = models.CharField(verbose_name="Наименование", max_length=255)
    wear_time = models.IntegerField(verbose_name="Сроки носки, мес.")
    nomenclature = models.CharField(verbose_name="Номенклатура", max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="Дата и время создания", auto_created=True, blank=True, null=True)
    last_modified = models.DateTimeField(verbose_name="Дата и время последнего изменения", auto_now=True, blank=True,
                                         null=True)

    def __str__(self):
        return self.clothes_title

    class Meta:
        ordering = ('id',)
        verbose_name = 'Наименование предмета'
        verbose_name_plural = 'Наименования предметов'


class Norm(models.Model):
    norm_title = models.CharField(verbose_name="Название нормы", max_length=255)
    clothes_list = models.ManyToManyField(Clothes, verbose_name="Наименования", through='ClothesInNorm', blank=True)
    created_at = models.DateTimeField(verbose_name="Дата и время создания", auto_created=True, blank=True, null=True)
    last_modified = models.DateTimeField(verbose_name="Дата и время последнего изменения", auto_now=True, blank=True,
                                         null=True)

    def __str__(self):
        return self.norm_title

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Норма'
        verbose_name_plural = 'Нормы'


class ClothesInNorm(models.Model):
    norm = models.ForeignKey(Norm, on_delete=models.CASCADE, verbose_name="Норма")
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE, verbose_name="Наименование")
    norm_count = models.IntegerField(verbose_name="Количество по норме")

    def __str__(self):
        return self.norm.norm_title + ' ' + self.clothes.clothes_title + ' ' + str(self.norm_count)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Наименование в норме'
        verbose_name_plural = 'Наименования в норме'


class Employee(models.Model):
    last_name = models.CharField(verbose_name="Фамилия", max_length=30)
    first_name = models.CharField(verbose_name="Имя", max_length=30, blank=True, null=True)
    patronymic = models.CharField(verbose_name="Отчество", max_length=30, blank=True, null=True)
    subdivision = models.ForeignKey(Subdivision, on_delete=models.SET_NULL, verbose_name="Подразделение", blank=True,
                                    null=True)
    sex = models.IntegerField(choices=SEX, verbose_name="Пол", blank=True, null=True)
    kind = models.IntegerField(choices=EMPLOYEE_KIND, verbose_name="Тип сотрудника")
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE, verbose_name="Звание", blank=True, null=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, verbose_name="Должность", blank=True, null=True)
    date_of_birth = models.DateField(verbose_name="Дата рождения", blank=True, null=True)
    last_modified = models.DateTimeField(verbose_name="Дата и время последнего редактирования", auto_now=True)

    def __str__(self):
        return self.last_name + ' ' + self.first_name + ' ' + self.patronymic

    @property
    def get_full_name(self):
        return self.last_name + ' ' + self.first_name + ' ' + self.patronymic

    @property
    def get_sex(self):
        if self.sex:
            return SEX[self.sex - 1][1]
        else:
            return None

    class Meta:
        ordering = ('last_name',)
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Card(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Сотрудник/курсант")
    norm = models.ForeignKey(Norm, on_delete=models.CASCADE, verbose_name="Норма")
    growth = models.IntegerField(verbose_name="Рост", blank=True, null=True)
    bust = models.IntegerField(verbose_name="Обхват груди", blank=True, null=True)
    jacket = models.IntegerField(choices=DIMENSIONS, verbose_name="Куртка", blank=True, null=True)
    shoes = models.IntegerField(choices=SHOES_DIMENSIONS, verbose_name="Обувь", blank=True, null=True)
    cap = models.IntegerField(verbose_name="Фуражка", blank=True, null=True)
    collar = models.IntegerField(choices=DIMENSIONS, verbose_name="Воротничок", blank=True, null=True)
    clothes = models.ManyToManyField(Clothes, verbose_name="Имущество", through='ClothesInCard', blank=True)
    created_at = models.DateTimeField(verbose_name="Дата и время создания", auto_created=True, blank=True, null=True)
    last_modified = models.DateTimeField(verbose_name="Дата и время последнего изменения", auto_now=True, blank=True,
                                         null=True)

    @property
    def get_jacket(self):
        if self.jacket:
            return DIMENSIONS[self.jacket - 1][1]
        else:
            return None

    @property
    def get_shoes(self):
        if self.jacket:
            return DIMENSIONS[self.shoes - 1][1]
        else:
            return None

    @property
    def get_collar(self):
        if self.jacket:
            return DIMENSIONS[self.collar - 1][1]
        else:
            return None

    def __str__(self):
        return self.employee.last_name

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Арматурная карточка'
        verbose_name_plural = 'Арматурные карточки'


class ClothesInCard(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, verbose_name="Арматурная карточка")
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE, verbose_name="Вещь")
    date_of_issue = models.DateField(verbose_name="Дата выдачи")
    created_at = models.DateTimeField(verbose_name="Дата и время создания", auto_created=True, blank=True, null=True)
    last_modified = models.DateTimeField(verbose_name="Дата и время последнего изменения", auto_now=True, blank=True,
                                         null=True)

    def __str__(self):
        return self.clothes.clothes_title + ' ' + str(self.date_of_issue)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Вещь в карточке'
        verbose_name_plural = 'Вещи в карточке'

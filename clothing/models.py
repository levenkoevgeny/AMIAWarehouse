from django.db import models
from django.core.validators import MinValueValidator

SEX = [
    (1, 'Мужской'),
    (2, 'Женский'),
]

EMPLOYEE_KIND = [
    (1, 'Курсант'),
    (2, 'Офицер'),
    (3, 'Гражданский'),
]

MOVEMENT = [
    (1, 'Выдача'),
    (2, 'Сдача'),
]


class Dimensions(models.Model):
    dimension = models.CharField(max_length=20, verbose_name="Размер")

    def __str__(self):
        return self.dimension

    class Meta:
        ordering = ('dimension',)
        verbose_name = 'Размер (куртки)'
        verbose_name_plural = 'Размеры (куртки)'


class ShoesDimensions(models.Model):
    shoes_dimension = models.CharField(max_length=20, verbose_name="Размер обуви")

    def __str__(self):
        return self.shoes_dimension

    class Meta:
        ordering = ('shoes_dimension',)
        verbose_name = 'Размер (обуви)'
        verbose_name_plural = 'Размеры (обуви)'


class CapDimensions(models.Model):
    cap_dimension = models.CharField(max_length=20, verbose_name="Размер фуражки")

    def __str__(self):
        return self.cap_dimension

    class Meta:
        ordering = ('cap_dimension',)
        verbose_name = 'Размер (фуражки)'
        verbose_name_plural = 'Размеры (фуражки)'


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
    nomenclature = models.CharField(verbose_name="Номенклатура", max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="Дата и время создания", auto_created=True, blank=True, null=True)
    price = models.FloatField(verbose_name="Цена", blank=True, null=True, validators=[MinValueValidator(0.0)])
    has_to_be_deposited = models.BooleanField(verbose_name="Подлежит сдаче", default=False)
    last_modified = models.DateTimeField(verbose_name="Дата и время последнего изменения", auto_now=True, blank=True,
                                         null=True)

    def __str__(self):
        return self.clothes_title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        NormItem.objects.create().item_clothes.add(self)

    # def delete(self, using=None, keep_parents=False):
    #     NormItem.objects.filter(item_clothes=self).delete()
    #     super().delete(using=None, keep_parents=False)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Наименование предмета'
        verbose_name_plural = 'Наименования предметов'


class NormItem(models.Model):
    item_clothes = models.ManyToManyField(Clothes, verbose_name="Совокупность вещей")

    def __str__(self):
        s = ""
        for clothes in self.item_clothes.all():
            s += clothes.clothes_title + "/ "
        return s[0:len(s) - 2]

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Позиция для нормы'
        verbose_name_plural = 'Позиции для нормы'


class Norm(models.Model):
    norm_title = models.CharField(verbose_name="Название нормы", max_length=255)
    items_list = models.ManyToManyField(NormItem, verbose_name="Наименования", through='NormItemsInNorm',
                                        blank=True)
    created_at = models.DateTimeField(verbose_name="Дата и время создания", auto_created=True, blank=True, null=True)
    last_modified = models.DateTimeField(verbose_name="Дата и время последнего изменения", auto_now=True, blank=True,
                                         null=True)

    def __str__(self):
        return self.norm_title

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Норма'
        verbose_name_plural = 'Нормы'


class NormItemsInNorm(models.Model):
    norm = models.ForeignKey(Norm, on_delete=models.CASCADE, verbose_name="Норма")
    norm_item = models.ForeignKey(NormItem, on_delete=models.CASCADE, verbose_name="Наименования")
    norm_count = models.IntegerField(verbose_name="Количество по норме")
    wear_time = models.IntegerField(verbose_name="Сроки носки, мес.", validators=[MinValueValidator(0)])

    def __str__(self):
        return self.norm.norm_title + ' ' + str(self.norm_item)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Наименование в норме'
        verbose_name_plural = 'Наименования в норме'
        unique_together = [['norm', 'norm_item']]


class Course(models.Model):
    course_name = models.CharField(verbose_name="Курс", max_length=255)

    def __str__(self):
        return self.course_name

    class Meta:
        ordering = ('course_name',)
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Group(models.Model):
    group_name = models.CharField(verbose_name="Группа", max_length=255)
    course = models.ForeignKey(Course, verbose_name="Курс", on_delete=models.SET_NULL, blank=True,
                               null=True)

    def __str__(self):
        return self.group_name

    class Meta:
        ordering = ('group_name',)
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Employee(models.Model):
    last_name = models.CharField(verbose_name="Фамилия", max_length=30)
    first_name = models.CharField(verbose_name="Имя", max_length=30)
    patronymic = models.CharField(verbose_name="Отчество", max_length=30)
    subdivision = models.ForeignKey(Subdivision, on_delete=models.SET_NULL, verbose_name="Подразделение", blank=True,
                                    null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, verbose_name="Группа", blank=True, null=True)
    sex = models.IntegerField(choices=SEX, verbose_name="Пол", blank=True, null=True, default=1)
    kind = models.IntegerField(choices=EMPLOYEE_KIND, verbose_name="Тип сотрудника")
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE, verbose_name="Звание", blank=True, null=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, verbose_name="Должность", blank=True, null=True)
    is_on_decree = models.BooleanField(verbose_name="В декрете", default=False)
    decree_start = models.DateField(verbose_name="Начало декрета", blank=True, null=True)
    decree_finish = models.DateField(verbose_name="Окончание декрета", blank=True, null=True)
    date_of_birth = models.DateField(verbose_name="Дата рождения", blank=True, null=True)
    enlisted = models.DateField(verbose_name="Зачислен", blank=True, null=True)
    excluded = models.DateField(verbose_name="Исключен", blank=True, null=True)
    personal_number = models.CharField(max_length=100, verbose_name="Персональный номер", blank=True, null=True)
    last_modified = models.DateTimeField(verbose_name="Дата и время последнего редактирования", auto_now=True)

    def __str__(self):
        return self.last_name

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
        ordering = ('-id',)
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Card(models.Model):
    card_number = models.CharField(max_length=100, verbose_name="Номер карты")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Сотрудник/курсант")
    norm = models.ForeignKey(Norm, on_delete=models.CASCADE, verbose_name="Норма")
    growth = models.IntegerField(verbose_name="Рост", blank=True, null=True)
    bust = models.IntegerField(verbose_name="Обхват груди", blank=True, null=True)
    jacket = models.ForeignKey(Dimensions, on_delete=models.SET_NULL, verbose_name="Куртка", blank=True, null=True)
    shoes = models.ForeignKey(ShoesDimensions, on_delete=models.SET_NULL, verbose_name="Обувь", blank=True, null=True)
    cap = models.ForeignKey(CapDimensions, on_delete=models.SET_NULL, verbose_name="Фуражка", blank=True, null=True)
    collar = models.ForeignKey(Dimensions, on_delete=models.SET_NULL, verbose_name="Воротничок", related_name="collar",
                               blank=True, null=True)
    # clothes = models.ManyToManyField(Clothes, verbose_name="Имущество", through='ClothesInCard', blank=True)
    created_at = models.DateTimeField(verbose_name="Дата и время создания", auto_created=True, blank=True, null=True)
    last_modified = models.DateTimeField(verbose_name="Дата и время последнего изменения", auto_now=True, blank=True,
                                         null=True)

    def __str__(self):
        return self.employee.last_name

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Арматурная карточка'
        verbose_name_plural = 'Арматурные карточки'


class Movement(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, verbose_name="Арматурная карточка")
    norm_item = models.ForeignKey(NormItem, on_delete=models.CASCADE, verbose_name="Позиция в норме")
    movement_description = models.ManyToManyField(Clothes, verbose_name="Описание движения наименований",
                                                  through='DescriptionItem', blank=True)
    date_of_issue = models.DateField(verbose_name="Дата выдачи/сдачи")
    movement_direction = models.IntegerField(choices=MOVEMENT, verbose_name="Движение (выдача / сдача)", default=1)
    has_replacement = models.BooleanField(verbose_name="Имеет замену", default=False)
    document_number = models.CharField(max_length=100, verbose_name="Номер документа", blank=True, null=True)
    has_certificate = models.BooleanField(verbose_name="Получено по сертификату", default=False)
    certificate_number = models.CharField(max_length=100, verbose_name="Номер аттестата", blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="Дата и время создания", auto_created=True, blank=True, null=True)
    is_closed_loop = models.BooleanField(verbose_name="Закрывает цикл выдачи", default=True)
    replacing_what = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name="Замена позиции из аттестата", blank=True, null=True)
    last_modified = models.DateTimeField(verbose_name="Дата и время последнего изменения", auto_now=True, blank=True,
                                         null=True)

    def __str__(self):
        return '{0} {1} {2}'.format(str(self.card), str(self.norm_item), str(self.date_of_issue))

    @property
    def get_movement(self):
        return MOVEMENT[self.movement - 1][1]

    class Meta:
        ordering = ('id',)
        verbose_name = 'Движение в карточке'
        verbose_name_plural = 'Движения в карточке'


class DescriptionItem(models.Model):
    movement = models.ForeignKey(Movement, on_delete=models.CASCADE,
                                 verbose_name="Движение в карточке")
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE, verbose_name="Наименование")
    count = models.IntegerField(verbose_name="Количество", default=1)

    def __str__(self):
        return '{0} {1}'.format(str(self.clothes), str(self.count))

    class Meta:
        ordering = ('id',)
        verbose_name = 'Описание движения в карточке'
        verbose_name_plural = 'Описания движений в карточке'
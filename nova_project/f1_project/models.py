from django.db import models


class Country(models.Model):
    country = models.CharField(
        max_length=42,
        verbose_name="Название страны"
    )
    country_abbr = models.CharField(
        max_length=3,
        verbose_name="Название страны, сокращенно"
    )
    flag = models.FileField(
        upload_to='flags/',
        null=True,
        blank=True,
        verbose_name="Флаг")

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural="Справочник стран"

    def __str__(self):
        return self.country


class Driver(models.Model):
    driver = models.CharField(
        max_length=42,
        verbose_name="Имя пилота"
    )
    driver_abbr = models.CharField(
        max_length=3,
        verbose_name="Имя пилота, сокращенно"
    )
    date_of_birth = models.DateField(
        verbose_name="Дата рождения пилота"
    )
    country = models.ForeignKey(
        'Country',
        on_delete=models.PROTECT,
        verbose_name="Страна"
    )

    class Meta:
        verbose_name = "Пилот"
        verbose_name_plural="Таблица пилотов"

    def __str__(self):
        return self.driver


class GrandPrix(models.Model):
    grand_prix = models.CharField(
        max_length=42,
        verbose_name="Название Гран При"
    )
    gp_abbr = models.CharField(
        max_length=3,
        verbose_name="Название Гран При, сокращенное"
    )
    country = models.ForeignKey(
        'Country',
        on_delete=models.PROTECT,
        verbose_name="Страна"
    )

    class Meta:
        verbose_name = "Гран При"
        verbose_name_plural = "Таблица Гран При"
    
    def __str__(self):
        return self.grand_prix


class Standing(models.Model):
    grand_prix = models.ForeignKey(
        'GrandPrix',
        on_delete=models.CASCADE,
        verbose_name="Гран При"
    )
    event_date = models.DateField(
        verbose_name="Дата проведения Гран При"
    )
    driver = models.ForeignKey(
        'Driver',
        on_delete=models.CASCADE,
        verbose_name="Пилот"
    )
    grd = models.IntegerField(
        verbose_name="Позиция на стартовой решетке"
    )
    pos = models.CharField(
        max_length=3,
        verbose_name="Позиция по итогам гонки"
    )
    pts = models.IntegerField(
        verbose_name="Количество заработанных очков"
    )
    pp = models.BooleanField(
        default=False,
        verbose_name="Поул позиция"
    )
    fl = models.BooleanField(
        default=False,
        verbose_name="Быстрый круг"
    )

    class Meta:
        verbose_name = "Результат гонки"
        verbose_name_plural = "Турнирная таблица"
    
    def __str__(self):
        return f"{self.grand_prix} - {self.driver}"


class Team(models.Model):
    team = models.CharField(
        max_length=42,
        verbose_name="Название команды"
    )
    team_abbr = models.CharField(
        max_length=3,
        verbose_name="Название команды, сокращенно"
    )
    country = models.ForeignKey(
        'Country',
        on_delete=models.PROTECT,
        verbose_name="Страна"
    )

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Таблица команд"
    
    def __str__(self):
        return self.team


class Transfer(models.Model):
    driver = models.ForeignKey(
        'Driver',
        on_delete=models.CASCADE,
        verbose_name="Пилот"
    )
    team = models.ForeignKey(
        'Team',
        on_delete=models.CASCADE,
        verbose_name="Команда"
    )
    start_date = models.DateField(
        verbose_name="Дата начала выступления за команду"
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата окончания выступления за команду"
    )

    class Meta:
        verbose_name = "Трансфер"
        verbose_name_plural = "Таблица перемещений пилотов"
    
    def __str__(self):
        return f"{self.driver} в {self.team} ({self.start_date})"
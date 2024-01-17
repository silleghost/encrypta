from django.db import models
from traitlets import default


class Categories(models.Model):
    name = models.CharField(
        max_length=150, unique=True, verbose_name="Название категории"
    )

    class Meta:
        db_table = "category"
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Passwords(models.Model):
    username = models.CharField(max_length=150, null=True, verbose_name="Имя пользователя")
    password = models.CharField(max_length=300, null=True, verbose_name="Пароль")

    class Meta:
        db_table = "password"
        verbose_name = "Пароль"
        verbose_name_plural = "Пароли"

    def __str__(self):
        return self.username


class Records(models.Model):
    app_name = models.CharField(max_length=150, verbose_name="Название приложения")
    urls = models.JSONField(default=dict, max_length=500, null=True, verbose_name="Адреса")
    records = models.ForeignKey(
        to=Passwords,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Сохраненные пароли",
    )
    category = models.ForeignKey(
        to=Categories, on_delete=models.SET_NULL, null=True, verbose_name="Категория"
    )
    notes = models.TextField(null=True, verbose_name="Заметки")
    creation_date = models.DateTimeField(
        auto_now_add=True, null=True, verbose_name="Дата создания"
    )
    lastmodified_date = models.DateTimeField(
        auto_now=True, null=True, verbose_name="Дата последнего изменения"
    )

    class Meta:
        db_table = "record"
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    def __str__(self):
        return self.app_name

from unicodedata import category
from django.db import models

from users.models import User


class Categories(models.Model):
    name = models.CharField(
        max_length=150, verbose_name="Название категории"
    )
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )

    class Meta:
        db_table = "category"
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"
        ordering = ("name",)

    def __str__(self):
        return f'{self.name} | {self.user.username}'


class Records(models.Model):
    app_name = models.CharField(max_length=150, verbose_name="Название приложения")
    username = models.CharField(
        max_length=150, null=True, verbose_name="Имя пользователя"
    )
    password = models.CharField(max_length=300, null=True, verbose_name="Пароль")
    favicon = models.ImageField(
        upload_to="favicon_images",
        blank=True,
        null=True,
        verbose_name="Иконка приложения",
    )
    url = models.CharField(max_length=500, blank=True, null=True, verbose_name="Адрес")
    category = models.ForeignKey(
        to=Categories,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Категория",
    )
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    # notes = models.TextField(blank=True, null=True, verbose_name="Заметки")
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
        return f'{self.category.name if self.category else "Без категории"} | {self.app_name} | {self.user.username}'

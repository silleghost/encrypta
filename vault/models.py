from django.db import models
from django.db.models.functions import Now


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название категории")

    class Meta:
        db_table = "category"
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Passwords(models.Model):
    app_name = models.CharField(max_length=150, verbose_name="Название приложения")
    username = models.CharField(max_length=150, verbose_name="Имя пользователя")
    password = models.JSONField(max_length=300, verbose_name="Пароль")
    urls = models.JSONField(max_length=500, verbose_name="Адреса")
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(db_default=Now())

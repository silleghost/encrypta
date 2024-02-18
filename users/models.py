from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        db_table = "user"
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class UserSettings(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    preferred_hash_algorithm = models.CharField(max_length=50)

    class Meta:
        db_table = "settings"
        verbose_name = "Настройки пользователей"
        verbose_name_plural= "Настройки пользователей"

    def __str__(self):
        return f"{self.user} | {self.preferred_hash_algorithm}"
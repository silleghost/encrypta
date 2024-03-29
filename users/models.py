from encrypta import settings
import jwt
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    username = models.CharField(unique=True, max_length=255, verbose_name="Имя пользователя")
    email = models.CharField(max_length=250, verbose_name="Электронная почта")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    is_staff = models.BooleanField(default=False, verbose_name="Персонал")
    date_joined = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Дата регистрации")
    last_login = models.DateTimeField(auto_now=True, null=True, verbose_name="Дата последнего входа")

    objects = UserManager()

    class Meta:
        indexes = [models.Index(fields=['username'])]
        db_table = "user"
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

    # def token(self):
    #     return self.__generate_jwt_token()
    
    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username
    
    # def __generate_jwt_token(self):
    #     dt = datetime.now() + timedelta(days=1)

    #     token = jwt.encode({
    #         'id': self.pk,
    #         'exp': int(dt.strftime('%s'))
    #     }, settings.SECRET_KEY, algorithm='HS256')

    #     return token.decode("utf-8")


class UserSettings(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    preferred_hash_algorithm = models.CharField(max_length=50, verbose_name="Алгоритм хеширования")

    class Meta:
        db_table = "settings"
        verbose_name = "Настройки пользователей"
        verbose_name_plural= "Настройки пользователей"

    def __str__(self):
        return f"{self.user} | {self.preferred_hash_algorithm}"
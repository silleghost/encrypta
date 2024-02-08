# Generated by Django 5.0 on 2024-02-08 09:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название категории')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Категорию',
                'verbose_name_plural': 'Категории',
                'db_table': 'category',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Records',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=150, verbose_name='Название приложения')),
                ('username', models.CharField(max_length=150, null=True, verbose_name='Имя пользователя')),
                ('password', models.CharField(max_length=300, null=True, verbose_name='Пароль')),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='favicon_images', verbose_name='Иконка приложения')),
                ('url', models.CharField(blank=True, max_length=500, null=True, verbose_name='Адрес')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('lastmodified_date', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата последнего изменения')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vault.categories', verbose_name='Категория')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Запись',
                'verbose_name_plural': 'Записи',
                'db_table': 'record',
            },
        ),
    ]

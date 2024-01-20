# Generated by Django 5.0 on 2024-01-20 07:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0003_alter_records_favicon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='records',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vault.categories', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='records',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='Заметки'),
        ),
    ]
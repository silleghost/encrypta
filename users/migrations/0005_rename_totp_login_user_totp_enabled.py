# Generated by Django 5.0 on 2024-04-02 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_totp_login_user_totp_secret'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='totp_login',
            new_name='totp_enabled',
        ),
    ]

# Generated by Django 3.2.5 on 2021-11-12 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_user_backup_codes_login_attempts'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User_BackUp_Codes_Login_Attempts',
        ),
    ]

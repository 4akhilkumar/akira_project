# Generated by Django 3.2.5 on 2021-11-14 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0014_user_backup_codes_login_attempts'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlogindetails',
            name='user_confirm',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
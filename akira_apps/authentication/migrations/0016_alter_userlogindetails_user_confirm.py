# Generated by Django 3.2.5 on 2021-11-16 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0015_userlogindetails_user_confirm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlogindetails',
            name='user_confirm',
            field=models.CharField(blank=True, default='Pending', max_length=100, null=True),
        ),
    ]

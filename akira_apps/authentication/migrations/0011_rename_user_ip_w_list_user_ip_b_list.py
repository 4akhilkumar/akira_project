# Generated by Django 3.2.5 on 2021-11-04 11:21

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0010_user_ip_w_list'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User_IP_W_List',
            new_name='User_IP_B_List',
        ),
    ]

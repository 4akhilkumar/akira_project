# Generated by Django 3.2.5 on 2021-11-12 05:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0008_user_backup_codes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_backup_codes',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
# Generated by Django 2.1.4 on 2018-12-22 15:57

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hunts', '0015_huntusers'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HuntUsers',
            new_name='HuntUser',
        ),
    ]
# Generated by Django 2.1.4 on 2018-12-18 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hunts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='puzzle',
            name='huntid',
            field=models.IntegerField(default='0', verbose_name='Hunt ID'),
        ),
        migrations.AddField(
            model_name='round',
            name='huntid',
            field=models.IntegerField(default='0', verbose_name='Hunt ID'),
        ),
    ]

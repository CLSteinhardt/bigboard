# Generated by Django 2.1.4 on 2018-12-18 23:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hunts', '0007_answer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hunt',
            old_name='name',
            new_name='huntname',
        ),
        migrations.RenameField(
            model_name='puzzle',
            old_name='name',
            new_name='puzzname',
        ),
        migrations.RenameField(
            model_name='round',
            old_name='name',
            new_name='roundname',
        ),
    ]

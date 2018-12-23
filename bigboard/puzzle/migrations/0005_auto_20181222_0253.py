# Generated by Django 2.1.4 on 2018-12-22 01:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hunts', '0014_auto_20181222_0222'),
        ('puzzle', '0004_auto_20181222_0236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='puzzid_id',
        ),
        migrations.AddField(
            model_name='tag',
            name='puzzid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hunts.Puzzle'),
        ),
    ]

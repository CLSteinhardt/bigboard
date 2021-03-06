# Generated by Django 2.1.4 on 2018-12-18 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hunts', '0005_auto_20181218_2153'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.AlterField(
            model_name='puzzle',
            name='huntid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hunts.Hunt'),
        ),
        migrations.AlterField(
            model_name='puzzround',
            name='puzzid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hunts.Puzzle'),
        ),
        migrations.AlterField(
            model_name='puzzround',
            name='roundid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hunts.Round'),
        ),
        migrations.AlterField(
            model_name='round',
            name='huntid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hunts.Hunt'),
        ),
    ]

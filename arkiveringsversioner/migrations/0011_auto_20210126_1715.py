# Generated by Django 3.1.5 on 2021-01-26 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arkiveringsversioner', '0010_auto_20210126_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='arkiveringsversion',
            name='public',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name='version',
            name='journaliseret',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='version',
            name='kopieret',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='version',
            name='kvitteret',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='version',
            name='stoerrelse',
            field=models.IntegerField(default=0, verbose_name='Størrelse i GB'),
        ),
        migrations.AlterField(
            model_name='arkiveringsversion',
            name='avid',
            field=models.IntegerField(),
        ),
    ]

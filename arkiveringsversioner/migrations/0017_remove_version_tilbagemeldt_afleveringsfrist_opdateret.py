# Generated by Django 3.1.5 on 2021-01-28 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arkiveringsversioner', '0016_auto_20210128_1403'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='version',
            name='tilbagemeldt_afleveringsfrist_opdateret',
        ),
    ]
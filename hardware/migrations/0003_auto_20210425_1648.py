# Generated by Django 3.1.5 on 2021-04-25 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0002_medie_arkiveringsversion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medie',
            old_name='arkiveringsversion',
            new_name='arkiveringsversioner',
        ),
    ]
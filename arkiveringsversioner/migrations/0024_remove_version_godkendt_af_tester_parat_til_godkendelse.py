# Generated by Django 3.1.5 on 2021-02-01 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arkiveringsversioner', '0023_auto_20210201_1158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='version',
            name='godkendt_af_tester_parat_til_godkendelse',
        ),
    ]

# Generated by Django 3.1.5 on 2021-01-26 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arkiveringsversioner', '0004_auto_20210126_1525'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Status',
        ),
        migrations.AddField(
            model_name='arkiveringsversion',
            name='arkivar_noter',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='arkiveringsversion',
            name='tester_noter',
            field=models.TextField(blank=True, null=True),
        ),
    ]

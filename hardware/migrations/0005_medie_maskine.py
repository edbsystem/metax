# Generated by Django 3.1.5 on 2021-04-26 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0004_auto_20210425_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='medie',
            name='maskine',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hardware.maskine'),
        ),
    ]

# Generated by Django 3.1.5 on 2021-01-26 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arkiveringsversioner', '0006_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='status',
            field=models.ManyToManyField(blank=True, related_name='_status_status_+', to='arkiveringsversioner.Status'),
        ),
    ]

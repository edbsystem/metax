# Generated by Django 3.1.5 on 2021-01-07 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bruger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Brugere',
            },
        ),
        migrations.CreateModel(
            name='Gruppe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('navn', models.CharField(blank=True, max_length=255, null=True)),
                ('bruger', models.ManyToManyField(blank=True, related_name='bruger', to='system.Bruger')),
            ],
            options={
                'verbose_name_plural': 'Grupper',
            },
        ),
        migrations.CreateModel(
            name='Profil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initialer', models.CharField(max_length=3, unique=True, verbose_name='initialer')),
                ('fornavn', models.CharField(blank=True, max_length=255, null=True, verbose_name='fornavn')),
                ('mellemnavn', models.CharField(blank=True, max_length=255, null=True, verbose_name='mellemnavn')),
                ('efternavn', models.CharField(blank=True, max_length=255, null=True, verbose_name='efternavn')),
            ],
            options={
                'verbose_name_plural': 'profiler',
            },
        ),
        migrations.CreateModel(
            name='Rettighed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('navn', models.CharField(choices=[('arkiveringsversioner_se', 'arkiveringsversioner_se'), ('hardware_se', 'hardware_se'), ('statistik_se', 'statistik_se'), ('system_se', 'system_se'), ('system_brugere_se', 'system_brugere_se'), ('system_bruger_se', 'system_bruger_se'), ('system_bruger_rediger', 'system_bruger_rediger'), ('system_grupper_se', 'system_grupper_se'), ('system_gruppe_se', 'system_gruppe_se'), ('system_gruppe_rediger', 'system_gruppe_rediger'), ('system_login', 'system_login'), ('system_profil_se', 'system_profil_se'), ('system_profil_rediger', 'system_profil_rediger')], max_length=255)),
                ('gruppe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.gruppe')),
            ],
            options={
                'verbose_name_plural': 'Rettigheder',
            },
        ),
        migrations.AddField(
            model_name='bruger',
            name='profil',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.profil'),
        ),
    ]

# Generated by Django 3.1.5 on 2021-01-28 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arkiveringsversioner', '0018_version_modtaget_ikke_krypteret'),
    ]

    operations = [
        migrations.RenameField(
            model_name='version',
            old_name='modtaget_ada_fejlet',
            new_name='modtaget_adatest_fejlet',
        ),
        migrations.RenameField(
            model_name='version',
            old_name='modtaget_afvikler_ada',
            new_name='modtaget_adatest_succesfuld',
        ),
        migrations.RemoveField(
            model_name='version',
            name='modtaget_klar_til_test',
        ),
    ]

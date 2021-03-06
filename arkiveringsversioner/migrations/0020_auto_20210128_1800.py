# Generated by Django 3.1.5 on 2021-01-28 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arkiveringsversioner', '0019_auto_20210128_1522'),
    ]

    operations = [
        migrations.RenameField(
            model_name='version',
            old_name='modtaget_adatest_fejlet',
            new_name='modtaget_adatest_afvist',
        ),
        migrations.RenameField(
            model_name='version',
            old_name='modtaget_adatest_succesfuld',
            new_name='modtaget_adatest_godkendt',
        ),
        migrations.AlterField(
            model_name='version',
            name='status',
            field=models.CharField(choices=[('Afventer aflevering', 'Afventer aflevering'), ('Modtaget', 'Modtaget'), ('Klar til test', 'Klar til test'), ('Under test', 'Under test'), ('Tilbagemeldt', 'Tilbagemeldt'), ('Afventer genaflevering', 'Afventer genaflevering'), ('Godkendt af tester', 'Godkendt af tester'), ('Godkendt', 'Godkendt')], default='Afventer aflevering', max_length=32),
        ),
    ]

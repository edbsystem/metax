from django.db import models

from system.models import Gruppe


class Rettighed(models.Model):
    RETTIGHED = (
        ('arkiveringsversioner_se', 'arkiveringsversioner_se'),

        ('hardware_se', 'hardware_se'),

        ('statistik_se', 'statistik_se'),

        ('system_se',                 'system_se'),

        ('system_brugere_se',         'system_brugere_se'),
        ('system_bruger_se',          'system_bruger_se'),
        ('system_bruger_rediger',     'system_bruger_rediger'),

        ('system_grupper_se',         'system_grupper_se'),
        ('system_gruppe_se',          'system_gruppe_se'),
        ('system_gruppe_rediger',     'system_gruppe_rediger'),

        ('system_login', 'system_login'),

        ('system_profil_se', 'system_profil_se'),
        ('system_profil_rediger', 'system_profil_rediger'),
    )

    navn = models.CharField(
        max_length=255,
        choices=RETTIGHED
    )

    gruppe = models.ForeignKey(
        to=Gruppe,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.navn)

    class Meta:
        verbose_name_plural = "Rettigheder"

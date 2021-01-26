from django.contrib.auth.models import User
from django.db import models

from .type import Type


class Arkiveringsversion(models.Model):

    KATEGORI = (
        ('Statslig', 'Statslig'),
        ('Kommunal', 'Kommunal'),
        ('Privat', 'Privat'),
        ('Forskningsdata', 'Forskningsdata')
    )

    KLASSIFIKATION = (
        ('Ingen', 'Ingen'),
        ('Til tjenestebrug', 'Til tjenestebrug'),
        ('Andet', 'Andet')
    )

    LAND = (
        ('Danmark', 'Danmark'),
        ('Grønland', 'Grønland')
    )

    avid = models.CharField(
        max_length=5,
        blank=False,
        null=False
    )

    jnr = models.CharField(
        max_length=32,
        blank=True,
        unique=True
    )

    titel = models.CharField(
        max_length=255,
        blank=True
    )

    kategori = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        choices=KATEGORI
    )

    klassifikation = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        choices=KLASSIFIKATION,
        default='Ingen'
    )

    type = models.ForeignKey(
        Type,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    land = models.CharField(
        max_length=8,
        null=True,
        blank=True,
        choices=LAND,
        default='Danmark',
    )

    arkivar_noter = models.TextField(
        null=True,
        blank=True,
    )

    tester_noter = models.TextField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.avid)

    class Meta:
        verbose_name_plural = "Arkiveringsversioner"

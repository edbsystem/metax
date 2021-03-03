from django.contrib.auth.models import User
from django.db import models

from .type import Type


class Arkiveringsversion(models.Model):

    KATEGORI = (
        ('Statslig', 'Statslig'),
        ('', 'Kommunal'),
        ('Privat', 'Privat'),
        ('Forskning', 'Forskning')
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

    avid = models.IntegerField(
        blank=False,
        null=False,
        unique=True
    )

    jnr = models.CharField(
        max_length=32,
        blank=True,
    )

    public = models.CharField(
        max_length=255,
        blank=True,
        null=True,
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

    afsluttet = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.avid)

    class Meta:
        verbose_name_plural = "Arkiveringsversioner"

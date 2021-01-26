from django.contrib.auth.models import User
from django.db import models

from .type import Type
from .status import Status
from .leverandoer import Leverandoer


class Arkiveringsversion(models.Model):
    VERSION = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (12, 12),
        (13, 13),
        (14, 14),
        (15, 15),
        (16, 16),
        (17, 17),
        (18, 18),
        (19, 19),
        (20, 20),
    )

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

    version = models.IntegerField(
        blank=False,
        null=False,
        choices=VERSION,
        default=1,
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

    status = models.ForeignKey(
        Status,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    leverandoer = models.ForeignKey(
        Leverandoer,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    afleveringsfrist = models.DateField(
        null=True,
        blank=True,
    )

    modtaget = models.DateField(
        null=True,
        blank=True,
    )

    adgang = models.DateField(
        null=True,
        blank=True,
    )

    svarfrist = models.DateField(
        null=True,
        blank=True,
    )

    svar = models.DateField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.avid)

    class Meta:
        verbose_name_plural = "Arkiveringsversioner"

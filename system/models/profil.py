from django.db import models

from .titel import Titel


class Profil(models.Model):
    initialer = models.CharField(
        max_length=3,
        blank=False,
        null=False,
        unique=True,
        verbose_name='initialer'
    )

    fornavn = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='fornavn'
    )

    mellemnavn = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='mellemnavn'
    )

    efternavn = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='efternavn'
    )

    titel = models.ForeignKey(
        Titel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return str(self.initialer)

    class Meta:
        verbose_name_plural = "Profiler"

from django.db import models

from .placering import Placering


class Maskine(models.Model):
    TYPE = (
        ('Server', 'Server'),
        ('Desktop', 'Desktop'),
        ('Laptop', 'Laptop')
    )

    navn = models.CharField(
        max_length=255,
        blank=True
    )

    processor = models.CharField(
        max_length=255,
        blank=True
    )

    bundkort = models.CharField(
        max_length=255,
        blank=True
    )

    arbejdshukommelse = models.IntegerField(
        default=0,
        verbose_name="Arbejdshukommelse i GB"
    )

    type = models.CharField(
        max_length=255,
        blank=True,
        choices=TYPE
    )

    kommentar = models.TextField(
        blank=True
    )

    placering = models.ForeignKey(
        Placering,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return str(self.navn)

    class Meta:
        verbose_name_plural = "Maskiner"

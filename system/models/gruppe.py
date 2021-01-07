from django.db import models

from system.models import Bruger


class Gruppe(models.Model):
    navn = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    bruger = models.ManyToManyField(
        Bruger,
        blank=True,
        related_name='bruger'
    )

    def __str__(self):
        return str(self.navn)

    class Meta:
        verbose_name_plural = "Grupper"

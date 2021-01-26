from django.db import models

from .profil import Profil


class Bruger(models.Model):
    profil = models.ForeignKey(
        Profil,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.profil)

    class Meta:
        verbose_name_plural = "Brugere"

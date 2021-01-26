from django.db import models


class Titel(models.Model):
    navn = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.navn)

    class Meta:
        verbose_name_plural = "Titler"

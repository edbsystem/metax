from django.db import models


class Type(models.Model):

    navn = models.CharField(
        max_length=255,
    )

    def __str__(self):
        return str(self.navn)

    class Meta:
        verbose_name_plural = "Typer"

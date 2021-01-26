from django.db import models


class Status(models.Model):

    navn = models.CharField(
        max_length=255,
    )

    status = models.ManyToManyField(
        'self',
        blank=True,
        related_name='statusser'
    )

    def __str__(self):
        return str(self.navn)

    class Meta:
        verbose_name_plural = "Statusser"

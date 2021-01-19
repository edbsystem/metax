from django.db import models


class Medie(models.Model):
    TYPE = (
        ('Solid State Drive', 'Solid State Drive'),
        ('Hard Drive 3.5', 'Hard Drive 3.5'),
        ('Hard Drive 2.5', 'Hard Drive 2.5'),
        ('USB Stick', 'USB Stick'),
        ('Ekstern SSD (USB)', 'Ekstern SSD (USB)'),
        ('Ekstern NVMe (USB)', 'Ekstern NVMe (USB)'),
        ('Ekstern Hard Drive (USB)', 'Ekstern Hard Drive (USB)'),
    )

    navn = models.CharField(
        max_length=255,
        blank=True,
    )

    producent = models.CharField(
        max_length=255,
        blank=True
    )

    kapacitet = models.IntegerField(
        default=0,
        verbose_name="Kapacitet i GB"
    )

    type = models.CharField(
        max_length=255,
        blank=True,
        choices=TYPE
    )

    def __str__(self):
        return self.navn

    class Meta:
        verbose_name_plural = "Medier"

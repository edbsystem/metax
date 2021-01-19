from django.db import models


class Placering(models.Model):
    LOKATION = (
        ('København', 'København'),
        ('Odense', 'Odense'),
    )

    LOKALE = (
        ('BLABLA01', 'Testværksted'),
        ('BLABLA02', 'Dataværksted'),
        ('BLABLA03', 'Kontor BLABLA03'),
    )

    NETVAERK = (
        ('SIT', 'SIT'),
        ('ARKNET', 'ARKNET'),
        ('Udvikling', 'Udvikling'),
    )

    lokation = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        choices=LOKATION,
    )

    lokale = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        choices=LOKALE,
    )

    netvaerk = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        choices=NETVAERK
    )

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name_plural = "Placeringer"

from django.db import models

from .arkiveringsversion import Arkiveringsversion
from .status import Status
from .leverandoer import Leverandoer


class Version(models.Model):

    NUMMER = (
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

    nummer = models.IntegerField(
        blank=False,
        null=False,
        choices=NUMMER,
        default=1,
    )

    avid = models.ForeignKey(
        Arkiveringsversion,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
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
        return str(self.nummer)

    class Meta:
        verbose_name_plural = "Versioner"

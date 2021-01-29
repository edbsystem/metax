from django.db import models

from .arkiveringsversion import Arkiveringsversion
from .status import Status
from .leverandoer import Leverandoer
from system.models import Bruger


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

    STATUS = (
        ('Afventer aflevering', 'Afventer aflevering'),
        ('Modtaget', 'Modtaget'),
        ('Klar til test', 'Klar til test'),
        ('Under test', 'Under test'),
        ('Tilbagemeldt', 'Tilbagemeldt'),
        ('Afventer genaflevering', 'Afventer genaflevering'),
        ('Godkendt af tester', 'Godkendt af tester'),
        ('Godkendt', 'Godkendt'),
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

    status = models.CharField(
        max_length=32,
        null=False,
        blank=False,
        choices=STATUS,
        default='Afventer aflevering',
    )

    tester = models.ForeignKey(
        Bruger,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='tester',
    )

    arkivar = models.ForeignKey(
        Bruger,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='arkivar',
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

    stoerrelse = models.IntegerField(
        default=0,
        verbose_name="Størrelse i GB"
    )

    modtaget_kvitteret = models.BooleanField(
        default=False,
    )

    modtaget_journaliseret = models.BooleanField(
        default=False,
    )

    modtaget_kodeord = models.BooleanField(
        default=False,
    )

    modtaget_mangler_kodeord = models.BooleanField(
        default=False,
    )

    modtaget_ikke_krypteret = models.BooleanField(
        default=False,
    )

    modtaget_kopieret = models.BooleanField(
        default=False,
    )

    modtaget_modtagelse_godkendt = models.BooleanField(
        default=False,
    )

    modtaget_modtagelse_afvist = models.BooleanField(
        default=False,
    )

    modtaget_fileindex_kopieret = models.BooleanField(
        default=False,
    )

    modtaget_adatest_godkendt = models.BooleanField(
        default=False,
    )

    modtaget_adatest_afvist = models.BooleanField(
        default=False,
    )

    tilbagemeldt_nedpakket = models.BooleanField(
        default=False,
    )

    tilbagemeldt_maskine_renset = models.BooleanField(
        default=False,
    )

    godkendt_af_tester_fileindex_godkendt = models.BooleanField(
        default=False,
    )

    godkendt_af_tester_afvikler_dea = models.BooleanField(
        default=False,
    )

    godkendt_af_tester_afleveret_til_dea = models.BooleanField(
        default=False,
    )

    godkendt_af_tester_retur_fra_dea = models.BooleanField(
        default=False,
    )

    godkendt_af_tester_mary_kontrol = models.BooleanField(
        default=False,
    )

    godkendt_af_tester_meta_opdateret = models.BooleanField(
        default=False,
    )

    godkendt_af_tester_public_opdateret = models.BooleanField(
        default=False,
    )

    godkendt_af_tester_nedpakket = models.BooleanField(
        default=False,
    )

    godkendt_af_tester_maskine_renset = models.BooleanField(
        default=False,
    )

    godkendt_af_tester_parat_til_godkendelse = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.nummer)

    class Meta:
        verbose_name_plural = "Versioner"

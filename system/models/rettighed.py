from django.db import models

from system.models import Gruppe


class Rettighed(models.Model):
    RETTIGHED = (
        ('arkiveringsversioner_se',                         'arkiveringsversioner_se'),
        ('arkiveringsversioner_arkiveringsversion_se',      'arkiveringsversioner_arkiveringsversion_se'),
        ('arkiveringsversioner_arkiveringsversion_rediger', 'arkiveringsversioner_arkiveringsversion_rediger'),
        ('arkiveringsversioner_arkiveringsversion_opret',   'arkiveringsversioner_arkiveringsversion_opret'),
        ('arkiveringsversioner_arkiveringsversion_slet',    'arkiveringsversioner_arkiveringsversion_slet'),

        ('arkiveringsversioner_avid_rediger', 'arkiveringsversioner_avid_rediger'),
        ('arkiveringsversioner_jnr_rediger', 'arkiveringsversioner_jnr_rediger'),
        ('arkiveringsversioner_public_rediger', 'arkiveringsversioner_public_rediger'),
        ('arkiveringsversioner_titel_rediger', 'arkiveringsversioner_titel_rediger'),
        ('arkiveringsversioner_kategori_rediger', 'arkiveringsversioner_kategori_rediger'),
        ('arkiveringsversioner_klassifikation_rediger', 'arkiveringsversioner_klassifikation_rediger'),
        ('arkiveringsversioner_typeav_rediger', 'arkiveringsversioner_typeav_rediger'),
        ('arkiveringsversioner_land_rediger', 'arkiveringsversioner_land_rediger'),
        ('arkiveringsversioner_arkivarnoter_rediger', 'arkiveringsversioner_arkivarnoter_rediger'),
        ('arkiveringsversioner_testernoter_rediger', 'arkiveringsversioner_testernoter_rediger'),
        ('arkiveringsversioner_afleveringsbestemmelse_rediger', 'arkiveringsversioner_afleveringsbestemmelse_rediger'),
        ('arkiveringsversioner_archiveindex_rediger', 'arkiveringsversioner_archiveindex_rediger'),
        ('arkiveringsversioner_contextdocumentationindex_rediger', 'arkiveringsversioner_contextdocumentationindex_rediger'),
        ('arkiveringsversioner_tester_rediger', 'arkiveringsversioner_tester_rediger'),
        ('arkiveringsversioner_arkivar_rediger', 'arkiveringsversioner_arkivar_rediger'),
        ('arkiveringsversioner_leverandør_rediger', 'arkiveringsversioner_leverandør_rediger'),
        ('arkiveringsversioner_afleveringsfrist_rediger', 'arkiveringsversioner_afleveringsfrist_rediger'),
        ('arkiveringsversioner_modtaget_rediger', 'arkiveringsversioner_modtaget_rediger'),
        ('arkiveringsversioner_adgang_rediger', 'arkiveringsversioner_adgang_rediger'),
        ('arkiveringsversioner_svarfrist_rediger', 'arkiveringsversioner_svarfrist_rediger'),
        ('arkiveringsversioner_svar_rediger', 'arkiveringsversioner_svar_rediger'),
        ('arkiveringsversioner_kvitteret_rediger', 'arkiveringsversioner_kvitteret_rediger'),
        ('arkiveringsversioner_journaliseret_rediger', 'arkiveringsversioner_journaliseret_rediger'),
        ('arkiveringsversioner_kopieret_rediger', 'arkiveringsversioner_kopieret_rediger'),
        ('arkiveringsversioner_størrelse_rediger', 'arkiveringsversioner_størrelse_rediger'),

        ('arkiveringsversioner_leverandører_se',    'arkiveringsversioner_leverandører_se'),
        ('arkiveringsversioner_leverandør_se',      'arkiveringsversioner_leverandør_se'),
        ('arkiveringsversioner_leverandør_rediger', 'arkiveringsversioner_leverandør_rediger'),
        ('arkiveringsversioner_leverandør_opret',   'arkiveringsversioner_leverandør_opret'),
        ('arkiveringsversioner_leverandør_slet',    'arkiveringsversioner_leverandør_slet'),

        ('arkiveringsversioner_typer_se',           'arkiveringsversioner_typer_se'),
        ('arkiveringsversioner_type_se',            'arkiveringsversioner_type_se'),
        ('arkiveringsversioner_type_rediger',       'arkiveringsversioner_type_rediger'),
        ('arkiveringsversioner_type_opret',         'arkiveringsversioner_type_opret'),
        ('arkiveringsversioner_type_slet',          'arkiveringsversioner_type_slet'),


        ('hardware_se',              'hardware_se'),

        ('hardware_maskiner_se',     'hardware_maskiner_se'),
        ('hardware_maskine_se',      'hardware_maskine_se'),
        ('hardware_maskine_rediger', 'hardware_maskine_rediger'),
        ('hardware_maskine_opret',   'hardware_maskine_opret'),
        ('hardware_maskine_slet',    'hardware_maskine_slet'),

        ('hardware_medier_se',     'hardware_medier_se'),
        ('hardware_medie_se',      'hardware_medie_se'),
        ('hardware_medie_rediger', 'hardware_medie_rediger'),
        ('hardware_medie_opret',   'hardware_medie_opret'),
        ('hardware_medie_slet',    'hardware_medie_slet'),


        ('statistik_se',           'statistik_se'),


        ('system_se',             'system_se'),

        ('system_brugere_se',     'system_brugere_se'),
        ('system_bruger_se',      'system_bruger_se'),
        ('system_bruger_rediger', 'system_bruger_rediger'),
        ('system_bruger_opret',   'system_bruger_opret'),
        ('system_bruger_slet',    'system_bruger_slet'),

        ('system_grupper_se',     'system_grupper_se'),
        ('system_gruppe_se',      'system_gruppe_se'),
        ('system_gruppe_rediger', 'system_gruppe_rediger'),
        ('system_gruppe_opret',   'system_gruppe_opret'),
        ('system_gruppe_slet',    'system_gruppe_slet'),

        ('system_logind',         'system_logind'),

        ('system_profil_se',      'system_profil_se'),
        ('system_profil_rediger', 'system_profil_rediger'),
    )

    navn = models.CharField(
        max_length=255,
        choices=RETTIGHED
    )

    gruppe = models.ForeignKey(
        Gruppe,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.navn)

    class Meta:
        verbose_name_plural = "Rettigheder"

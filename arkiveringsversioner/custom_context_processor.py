from django.db.models.functions import Lower

from arkiveringsversioner.models import Arkiveringsversion, Type, Leverandoer, Version
from system.models import Titel, Profil


def subject_renderer(request):

    _kategorier = []
    for _kategori in list(Arkiveringsversion._meta.get_field('kategori').choices):
        _kategorier.append(_kategori[1])

    _klassifikationer = []
    for _klassifikation in list(Arkiveringsversion._meta.get_field('klassifikation').choices):
        _klassifikationer.append(_klassifikation[1])

    _typer = []
    for _type_obj in Type.objects.all():
        _typer.append(_type_obj.navn)

    _lande = []
    for _land in list(Arkiveringsversion._meta.get_field('land').choices):
        _lande.append(_land[1])

    _leverandoerer = []
    for _leverandoer_obj in Leverandoer.objects.all():
        _leverandoerer.append(_leverandoer_obj.navn)

    _statusser = []
    for _status in list(Version._meta.get_field('status').choices):
        _statusser.append(_status[1])
    _statusser.append('Afsluttet')

    _arkiveringsversioner = Arkiveringsversion.objects.all()

    return {
        "kategorier": _kategorier,
        "klassifikationer": _klassifikationer,
        "typer": sorted(_typer, key=lambda _type: _type[0]),
        "lande": _lande,
        "leverandoerer": _leverandoerer,
        "arkiveringsversioner": _arkiveringsversioner,
        "statusser": _statusser
    }

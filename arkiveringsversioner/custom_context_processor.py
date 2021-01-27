from django.db.models.functions import Lower

from arkiveringsversioner.models import Arkiveringsversion, Type


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

    return {
        "kategorier": _kategorier,
        "klassifikationer": _klassifikationer,
        "typer": sorted(_typer, key=lambda _type: _type[0]),
        "lande": _lande,
    }

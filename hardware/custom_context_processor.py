from django.db.models.functions import Lower

from hardware.models import Medie, Maskine, Placering


def subject_renderer(request):

    _medie_typer = []
    for medie_type in list(Medie._meta.get_field('type').choices):
        _medie_typer.append(medie_type[1])

    _maskine_typer = []
    for maskine_type in list(Maskine._meta.get_field('type').choices):
        _maskine_typer.append(maskine_type[1])

    _lokationer = []
    for lokation in list(Placering._meta.get_field('lokation').choices):
        _lokationer.append(lokation[1])

    _lokaler = []
    for lokale in list(Placering._meta.get_field('lokale').choices):
        _lokaler.append(lokale[1])

    _netvaerker = []
    for netvaerk in list(Placering._meta.get_field('netvaerk').choices):
        _netvaerker.append(netvaerk[1])

    return {
        "medie_typer": sorted(_medie_typer),
        "maskine_typer": sorted(_maskine_typer),
        "lokationer": sorted(_lokationer),
        "lokaler": sorted(_lokaler),
        "netvaerker": sorted(_netvaerker),
    }

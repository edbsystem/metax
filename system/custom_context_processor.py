from django.db.models.functions import Lower

from system.models import Gruppe, Rettighed, Bruger


def subject_renderer(request):

    _grupper = []
    for gruppe in Gruppe.objects.all().order_by(Lower('navn')):
        _grupper.append(gruppe.navn)

    _rettigheder = []
    for rettighed in list(Rettighed._meta.get_field('navn').choices):
        _rettigheder.append(rettighed[1])

    _brugere = []
    for _bruger in Bruger.objects.all():

        _initialer = _bruger.profil.initialer
        _fuldenavn = ''

        if _bruger.profil.fornavn != '' and _bruger.profil.fornavn != None:
            _fuldenavn += str(_bruger.profil.fornavn)
        if _bruger.profil.mellemnavn != '' and _bruger.profil.mellemnavn != None:
            _fuldenavn += ' '
            _fuldenavn += str(_bruger.profil.mellemnavn)
        if _bruger.profil.efternavn != '' and _bruger.profil.efternavn != None:
            _fuldenavn += ' '
            _fuldenavn += str(_bruger.profil.efternavn)

        _brugere.append([_initialer, _fuldenavn])

    return {
        "grupper": _grupper,
        "rettigheder": _rettigheder,
        "brugere": sorted(_brugere),
    }

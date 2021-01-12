from system.models import Gruppe, Rettighed, Bruger


def subject_renderer(request):

    _grupper = []
    for gruppe_obj in Gruppe.objects.all():
        _grupper.append(gruppe_obj.navn)

    _rettigheder = []
    for rettighed in list(Rettighed._meta.get_field('navn').choices):
        _rettigheder.append(rettighed[1])

    _brugere = []
    for _bruger_obj in Bruger.objects.all():

        _initialer = _bruger_obj.profil.initialer
        _fuldenavn = ''

        if _bruger_obj.profil.fornavn != '' and _bruger_obj.profil.fornavn != None:
            _fuldenavn += _bruger_obj.profil.fornavn
        if _bruger_obj.profil.mellemnavn != '' and _bruger_obj.profil.mellemnavn != None:
            _fuldenavn += ' '
            _fuldenavn += _bruger_obj.profil.mellemnavn
        if _bruger_obj.profil.efternavn != '' and _bruger_obj.profil.efternavn != None:
            _fuldenavn += ' '
            _fuldenavn += _bruger_obj.profil.efternavn

        _brugere.append([_initialer, _fuldenavn])

    return {
        "grupper": sorted(_grupper),
        "rettigheder": sorted(_rettigheder),
        "brugere": sorted(_brugere, key=lambda _bruger: _bruger[0]),
    }

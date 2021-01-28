from system.models import Gruppe, Rettighed, Bruger, Titel, Profil


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

    _testere = []
    _titel_obj = Titel.objects.get(navn='Tester')
    for _profil_obj in Profil.objects.filter(titel=_titel_obj):

        _fuldenavn = ''

        if _profil_obj.fornavn != '' and _profil_obj.fornavn != None:
            _fuldenavn += _profil_obj.fornavn
        if _profil_obj.mellemnavn != '' and _profil_obj.mellemnavn != None:
            _fuldenavn += ' '
            _fuldenavn += _profil_obj.mellemnavn
        if _profil_obj.efternavn != '' and _profil_obj.efternavn != None:
            _fuldenavn += ' '
            _fuldenavn += _profil_obj.efternavn

        _testere.append(_fuldenavn)

    _arkivarer = []
    _titel_obj = Titel.objects.get(navn='Arkivar')
    for _profil_obj in Profil.objects.filter(titel=_titel_obj):

        _fuldenavn = ''

        if _profil_obj.fornavn != '' and _profil_obj.fornavn != None:
            _fuldenavn += _profil_obj.fornavn
        if _profil_obj.mellemnavn != '' and _profil_obj.mellemnavn != None:
            _fuldenavn += ' '
            _fuldenavn += _profil_obj.mellemnavn
        if _profil_obj.efternavn != '' and _profil_obj.efternavn != None:
            _fuldenavn += ' '
            _fuldenavn += _profil_obj.efternavn

        _arkivarer.append(_fuldenavn)

    return {
        "grupper": sorted(_grupper),
        "rettigheder": _rettigheder,
        "brugere": sorted(_brugere, key=lambda _bruger: _bruger[0]),
        "testere": sorted(_testere),
        "arkivarer": sorted(_arkivarer),
    }

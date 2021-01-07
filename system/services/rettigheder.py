from system.models import Profil, Bruger, Gruppe, Rettighed


def rettigheder(user):

    _profil = Profil.objects.get(initialer=str(user))
    _bruger = Bruger.objects.get(profil=_profil)

    _rettigheder = set()

    for _gruppe in Gruppe.objects.all():
        if _gruppe.bruger.filter(profil=_profil).first():
            for _rettighed in Rettighed.objects.filter(gruppe=_gruppe):
                _rettigheder.add(_rettighed.navn)

    return _rettigheder

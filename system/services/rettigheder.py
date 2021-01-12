from system.models import Profil, Bruger, Gruppe, Rettighed


def rettigheder(user):

    _rettigheder = set()

    if Profil.objects.filter(initialer=user).exists():
        _profil_obj = Profil.objects.get(initialer=user)
        _bruger_obj = Bruger.objects.get(profil=_profil_obj)

        for _gruppe_obj in Gruppe.objects.all():
            if _gruppe_obj.bruger.filter(profil=_profil_obj).first():
                for _rettighed_obj in Rettighed.objects.filter(gruppe=_gruppe_obj):
                    _rettigheder.add(_rettighed_obj.navn)

    return list(_rettigheder)

from system.models import Profil, Bruger, Gruppe, Rettighed
from system.services import rettigheder


def tjek_rettigheder(user, rttghdr):

    if not user.is_authenticated:
        return False

    _rettigheder = rettigheder(user)

    if not rttghdr.issubset(_rettigheder):
        return False

    return True

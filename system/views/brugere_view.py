from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models.functions import Lower

from system.models import Bruger
from system.services import rettigheder, tjek_rettigheder


def tjek(user):
    return tjek_rettigheder(user, {'system_brugere_se'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def brugere_view(request):

    _brugere = Bruger.objects.all().order_by(Lower('profil'))

    return render(request, 'system/brugere.html', {
        "bruger_rettigheder": list(rettigheder(request.user)),
        "brugere": _brugere,
    })

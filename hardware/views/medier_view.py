from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models.functions import Lower

from hardware.models import Medie
from system.services import rettigheder, tjek_rettigheder


def tjek(user):
    return tjek_rettigheder(user, {'hardware_medier_se'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def medier_view(request):

    _medier_objs = sorted(Medie.objects.all(), key=lambda _medie: _medie.navn)

    return render(request, 'hardware/medier.html', {
        "bruger_rettigheder": rettigheder(request.user),
        "medier": _medier_objs,
    })

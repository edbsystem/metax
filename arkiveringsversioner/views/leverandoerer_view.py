from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

from arkiveringsversioner.models import Leverandoer
from system.services import rettigheder, tjek_rettigheder


def tjek(user):
    return tjek_rettigheder(user, {'arkiveringsversioner_leverandører_se'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def leverandoerer_view(request):

    _leverandoerer_objs = sorted(Leverandoer.objects.all(), key=lambda _leverandoer: _leverandoer.navn)

    return render(request, 'arkiveringsversioner/leverandoerer.html', {
        "bruger_rettigheder": rettigheder(request.user),
        "leverandoerer": _leverandoerer_objs,
    })

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

from system.services import rettigheder, tjek_rettigheder
from hardware.models import Maskine


def tjek(user):
    return tjek_rettigheder(user, {'hardware_maskiner_se'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def maskiner_view(request):

    _maskiner_objs = sorted(Maskine.objects.all(), key=lambda _maskine: _maskine.navn)

    return render(request, 'hardware/maskiner.html', {
        "bruger_rettigheder": rettigheder(request.user),
        "maskiner": _maskiner_objs,
    })

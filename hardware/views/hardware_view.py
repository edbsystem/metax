from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

from system.services import rettigheder, tjek_rettigheder


def tjek(user):
    return tjek_rettigheder(user, {'hardware_se'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def hardware_view(request):
    return render(request, 'hardware/hardware.html', {
        "bruger_rettigheder": list(rettigheder(request.user)),
    })

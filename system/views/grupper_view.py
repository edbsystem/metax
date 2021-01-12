from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models.functions import Lower

from system.models.gruppe import Gruppe
from system.services import rettigheder, tjek_rettigheder


def tjek(user):
    return tjek_rettigheder(user, {'system_grupper_se'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def grupper_view(request):

    _grupper = Gruppe.objects.all().order_by(Lower('navn'))

    return render(request, 'system/grupper.html', {
        "bruger_rettigheder": rettigheder(request.user),
        "grupper": _grupper,
    })

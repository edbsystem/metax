from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

from system.services import rettigheder, tjek_rettigheder


def tjek(user):
    return tjek_rettigheder(user, {'system_se'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def system_view(request):
    return render(request, 'system/system.html', {
        "bruger_rettigheder": list(rettigheder(request.user)),
    })

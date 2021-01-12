from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

from system.services import rettigheder, tjek_rettigheder


def tjek(user):
    return tjek_rettigheder(user, {'system_logind'})


@user_passes_test(tjek, login_url='/system/logind', redirect_field_name=None)
def forside_view(request):
    return render(request, 'forside/forside.html', {
        "bruger_rettigheder": rettigheder(request.user)
    })

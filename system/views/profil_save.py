from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test

from system.models import Profil, Bruger, Gruppe
from system.services import rettigheder, tjek_rettigheder


def tjek(user):
    return tjek_rettigheder(user, {'system_profil_rediger'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def profil_save(request, initialer=None):

    if request.method == 'POST':

        return render(request, 'profil.html', {
            "bruger_rettigheder": list(rettigheder(request.user))
        })

    return redirect('forside_view')

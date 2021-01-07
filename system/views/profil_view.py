from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test

from system.models import Profil, Bruger, Gruppe
from system.services import rettigheder, tjek_rettigheder


def tjek(user):
    return tjek_rettigheder(user, {'system_profil_se'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def profil_view(request, initialer=None):

    if request.method == 'GET':

        if Profil.objects.filter(initialer=request.user.username).exists():
            profil = Profil.objects.get(initialer=request.user.username)

            return render(request, 'profil.html', {
                "bruger_rettigheder": list(rettigheder(request.user)),
                "profil": profil
            })

    return redirect('forside_view')

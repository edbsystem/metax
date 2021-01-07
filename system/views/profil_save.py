from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages

from system.models import Profil, Bruger, Gruppe
from system.services import rettigheder, tjek_rettigheder


def tjek(user):
    return tjek_rettigheder(user, {'system_profil_rediger'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def profil_save(request, initialer=None):

    if request.method == 'POST':

        if Profil.objects.filter(initialer=request.user.username).exists():
            _profil = Profil.objects.get(initialer=request.user.username)
            _bruger = User.objects.get(username=request.user.username)

            _nuvaerende_adgangskode = request.POST['nuvaerende_adgangskode'] if 'nuvaerende_adgangskode' in request.POST else None
            _ny_adgangskode = request.POST['ny_adgangskode'] if 'ny_adgangskode' in request.POST else None
            _bekraeft_adgangskode = request.POST['bekraeft_adgangskode'] if 'bekraeft_adgangskode' in request.POST else None

            _check_nuvaerende_adgangskode = False
            _check_ny_og_bekraeft_adgangskode = False

        return render(request, 'profil.html', {
            "bruger_rettigheder": list(rettigheder(request.user))
        })

    return redirect('forside_view')

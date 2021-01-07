from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages

from system.models import Profil
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

    if request.method == 'POST' and tjek_rettigheder(request.user, {'system_profil_rediger'}):

        if Profil.objects.filter(initialer=request.user.username).exists():

            _profil = Profil.objects.get(initialer=request.user.username)
            _bruger = User.objects.get(username=request.user.username)

            _nuvaerende_adgangskode = request.POST['nuvaerende_adgangskode'] if 'nuvaerende_adgangskode' in request.POST else None
            _ny_adgangskode = request.POST['ny_adgangskode'] if 'ny_adgangskode' in request.POST else None
            _bekraeft_adgangskode = request.POST['bekraeft_adgangskode'] if 'bekraeft_adgangskode' in request.POST else None

            _check_nuvaerende_adgangskode = False
            _check_ny_og_bekraeft_adgangskode = False

            if _nuvaerende_adgangskode:
                if _bruger.check_password(_nuvaerende_adgangskode):
                    _check_nuvaerende_adgangskode = True
                else:
                    messages.error(request, "'Nuværende' adgangkode er forkert.")
            else:
                messages.error(request, "Feltet 'Nuværende' er tomt.")

            if not _ny_adgangskode:
                messages.error(request, "Feltet 'Ny' er tomt.")

            if not _bekraeft_adgangskode:
                messages.error(request, "Feltet 'Bekræft' er tomt.")

            if _ny_adgangskode and _bekraeft_adgangskode:
                if _ny_adgangskode == _bekraeft_adgangskode:
                    _check_ny_og_bekraeft_adgangskode = True
                else:
                    messages.error(request, "'Ny' afgangskode og 'Bekræft' adgangskode stemmer ikke overens.")

            if _check_nuvaerende_adgangskode and _check_ny_og_bekraeft_adgangskode:
                _bruger.set_password(_ny_adgangskode)
                _bruger.save()
                return redirect('login_view')

            return render(request, 'profil.html', {
                "bruger_rettigheder": list(rettigheder(request.user)),
                "profil": _profil,
                "nuvaerende_adgangskode": _nuvaerende_adgangskode,
                "ny_adgangskode": _ny_adgangskode,
                "bekraeft_adgangskode": _bekraeft_adgangskode,
            })

    return redirect('forside_view')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test

from system.models import Profil, Bruger, Gruppe, Rettighed
from system.services import rettigheder, tjek_rettigheder


def tjek(user):
    return tjek_rettigheder(user, {'system_gruppe_se'})


@ user_passes_test(tjek, login_url='/', redirect_field_name=None)
def gruppe_view(request, navn=None):

    if request.method == 'GET':

        if navn:

            if Gruppe.objects.filter(navn=navn).exists():
                _gruppe_obj = Gruppe.objects.get(navn=navn)

                _tildelte_rettigheder = []
                for rettighed in Gruppe.objects.get(navn=navn).rettighed_set.all():
                    _tildelte_rettigheder.append(rettighed.navn)

                _tildelte_brugere = []
                for _bruger_obj in _gruppe_obj.bruger.all():
                    _tildelte_brugere.append(_bruger_obj.profil.initialer)

                return render(request, 'system/gruppe.html', {
                    "bruger_rettigheder": rettigheder(request.user),
                    "navn": _gruppe_obj.navn,
                    "tildelte_rettigheder": sorted(_tildelte_rettigheder),
                    "tildelte_brugere": sorted(_tildelte_brugere),
                    "ny": False,
                    "slet": True,
                })

            if not Gruppe.objects.filter(navn=navn).exists():
                messages.error(request, "Den angivet gruppe findes ikke.")
                return redirect('grupper_view')

        if not navn:
            return render(request, 'system/gruppe.html', {
                "bruger_rettigheder": rettigheder(request.user),
                "navn": '',
                "ny": True,
                "slet": False,
            })

    if request.method == 'POST' and tjek_rettigheder(request.user, {'system_gruppe_rediger'}):

        if 'fortryd' in request.POST:
            return redirect('grupper_view')

        _ny = request.POST['ny'] if 'ny' in request.POST else 'False'
        _navn = request.POST['navn'].upper().strip() if 'navn' in request.POST else None

        if _navn:

            if Gruppe.objects.filter(navn=_navn).exists():

                if 'slet' in request.POST and tjek_rettigheder(request.user, {'system_gruppe_slet'}):
                    _gruppe_obj = Gruppe.objects.get(navn=_navn)
                    _gruppe_obj.delete()

                    messages.warning(request, f"Gruppen '{_navn}' blev slettet.")
                    return redirect('grupper_view')

                if _ny == 'True':
                    messages.error(request, f"Gruppen '{_navn}' findes allerede.")
                    return render(request, 'system/gruppe.html', {
                        "bruger_rettigheder": rettigheder(request.user),
                        "navn": _navn,
                        "ny": True,
                        "slet": False,
                    })

                if _ny == 'False':
                    _gruppe_obj = Gruppe.objects.get(navn=_navn)
                    _gruppe_obj.navn = _navn if _navn != '' else _gruppe_obj.navn

                    _rettigheder = []
                    for _rettighed in list(Rettighed._meta.get_field('navn').choices):
                        _rettigheder.append(_rettighed[1])

                    for _rettighed in _rettigheder:
                        _post_rettighed = request.POST[_rettighed] if _rettighed in request.POST else None

                        if _post_rettighed:
                            if not Rettighed.objects.filter(navn=_rettighed, gruppe=_gruppe_obj).first():
                                Rettighed.objects.create(navn=_rettighed, gruppe=_gruppe_obj)

                        if not _post_rettighed:
                            _rettighed_obj = Rettighed.objects.filter(navn=_rettighed, gruppe=_gruppe_obj).first()
                            if _rettighed_obj:
                                _rettighed_obj.delete()

                    _gruppe_obj.save()

                    messages.success(request, f"Gruppen '{_navn}' blev gemt.")
                    return redirect('grupper_view')

            if not Gruppe.objects.filter(navn=_navn).exists() and tjek_rettigheder(request.user, {'system_gruppe_opret'}):
                Gruppe.objects.create(navn=_navn)

                messages.success(request, f"Gruppen '{_navn}' blev oprettet.")
                return render(request, 'system/gruppe.html', {
                    "bruger_rettigheder": rettigheder(request.user),
                    "navn": _navn,
                    "ny": False,
                    "slet": True,
                })

        if not _navn:
            messages.error(request, f"Udfyld venligst feltet 'Navn'.")
            return render(request, 'system/gruppe.html', {
                "bruger_rettigheder": rettigheder(request.user),
                "navn": _navn,
                "ny": True,
                "slet": False,
            })

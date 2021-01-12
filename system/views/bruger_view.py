from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User

from system.models import Profil, Bruger, Gruppe
from system.services import rettigheder, tjek_rettigheder


def tjek(user):
    return tjek_rettigheder(user, {'system_bruger_se'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def bruger_view(request, initialer=None):

    if request.method == 'GET':

        if initialer:

            _slet = True

            if Profil.objects.filter(initialer=initialer).exists():
                _profil_obj = Profil.objects.get(initialer=initialer)
                _bruger_obj = Bruger.objects.get(profil=_profil_obj)

                _tildelte_grupper = []
                for _gruppe_obj in Gruppe.objects.filter(bruger=_bruger_obj):
                    _tildelte_grupper.append(_gruppe_obj.navn)

                return render(request, 'system/bruger.html', {
                    "bruger_rettigheder": list(rettigheder(request.user)),
                    "initialer": _bruger_obj.profil.initialer,
                    "fornavn": _bruger_obj.profil.fornavn,
                    "mellemnavn": _bruger_obj.profil.mellemnavn,
                    "efternavn": _bruger_obj.profil.efternavn,
                    "adgangskode": '',
                    "tildelte_grupper": sorted(_tildelte_grupper),
                    "ny": False,
                    "slet": _slet,
                })

            if not Profil.objects.filter(initialer=initialer).exists():
                messages.error(request, "Den angivet bruger findes ikke.")
                return redirect('brugere_view')

        if not initialer:
            return render(request, 'system/bruger.html', {
                "bruger_rettigheder": list(rettigheder(request.user)),
                "initialer": '',
                "fornavn": '',
                "mellemnavn": '',
                "efternavn": '',
                "adgangskode": '',
                "ny": True,
                "slet": False,
            })

    if request.method == 'POST' and tjek_rettigheder(request.user, {'system_bruger_rediger'}):

        if 'fortryd' in request.POST:
            return redirect('brugere_view')

        _ny = request.POST['ny'] if 'ny' in request.POST else 'False'
        _initialer = request.POST['initialer'].upper() if 'initialer' in request.POST else None
        _fornavn = request.POST['fornavn'] if 'fornavn' in request.POST else None
        _mellemnavn = request.POST['mellemnavn'] if 'mellemnavn' in request.POST else None
        _efternavn = request.POST['efternavn'] if 'efternavn' in request.POST else None
        _adgangskode = request.POST['adgangskode'] if 'adgangskode' in request.POST else None

        if _initialer:
            if len(_initialer) != 3:

                _grupper = []
                for _gruppe_obj in Gruppe.objects.all():
                    _grupper.append(_gruppe_obj.navn)

                _tildelte_grupper = []
                for _gruppe in _grupper:
                    if _gruppe in request.POST:
                        _tildelte_grupper.append(_gruppe)

                messages.error(request, f"Initialer skal altid udgøres af tre tegn. Hverken mere eller mindre. Tre tegn!")
                return render(request, 'system/bruger.html', {
                    "bruger_rettigheder": list(rettigheder(request.user)),
                    "initialer": _initialer,
                    "fornavn": _fornavn,
                    "mellemnavn": _mellemnavn,
                    "efternavn": _efternavn,
                    "adgangskode": '',
                    "tildelte_grupper": sorted(_tildelte_grupper),
                    "ny": True,
                    "slet": False,
                })

            if Profil.objects.filter(initialer=_initialer).exists():

                if 'slet' in request.POST:
                    messages.warning(request, f"Brugeren '{_initialer}' blev slettet.")

                    _user_obj = User.objects.get(username=_initialer)
                    _profil_obj = Profil.objects.get(initialer=_initialer)
                    _bruger_obj = Bruger.objects.get(profil=_profil_obj)

                    _user_obj.delete()
                    _bruger_obj.delete()
                    _profil_obj.delete()

                    return redirect('brugere_view')

                if _ny == 'True':
                    messages.error(request, f"Brugeren '{_initialer}' findes allerede.")

                    return render(request, 'system/bruger.html', {
                        "bruger_rettigheder": list(rettigheder(request.user)),
                        "fornavn": _fornavn,
                        "mellemnavn": _mellemnavn,
                        "efternavn": _efternavn,
                        "adgangskode": '',
                        "ny": True,
                        "slet": False,
                    })

                if not _ny == 'True':
                    _profil_obj = Profil.objects.get(initialer=_initialer)
                    _bruger_obj = Bruger.objects.get(profil=_profil_obj)

                    _bruger_obj.profil.fornavn = _fornavn if _fornavn != '' else _bruger_obj.profil.fornavn
                    _bruger_obj.profil.mellemnavn = _mellemnavn if _mellemnavn != '' else _bruger_obj.profil.mellemnavn
                    _bruger_obj.profil.efternavn = _efternavn if _efternavn != '' else _bruger_obj.profil.efternavn
                    _bruger_obj.profil.save()

                    if _adgangskode != '':
                        _user_obj = User.objects.get(username=_initialer)
                        _user_obj.set_password(_adgangskode)
                        _user_obj.save()

                    _grupper = []
                    for gruppe_obj in Gruppe.objects.all():
                        _grupper.append(gruppe_obj.navn)

                    for _gruppe in _grupper:
                        _post_gruppe = request.POST[_gruppe] if _gruppe in request.POST else None

                        if _post_gruppe:
                            if not Gruppe.objects.filter(navn=_gruppe, bruger=_bruger_obj).first():
                                _gruppe_obj = Gruppe.objects.get(navn=_gruppe)
                                _gruppe_obj.bruger.add(_bruger_obj)

                        if not _post_gruppe:
                            _gruppe_obj = Gruppe.objects.filter(navn=_gruppe, bruger=_bruger_obj).first()
                            if _gruppe_obj:
                                _gruppe_obj.bruger.remove(_bruger_obj)

                    messages.success(request, f"Brugeren '{_initialer}' blev gemt.")
                    return redirect('brugere_view')

            if not Profil.objects.filter(initialer=_initialer).exists():
                User.objects.create_user(username=_initialer)
                _profil_obj = Profil.objects.create(initialer=_initialer)
                _bruger_obj = Bruger.objects.create(profil=_profil_obj)

                _bruger_obj.profil.fornavn = _fornavn if _fornavn != '' else _bruger_obj.profil.fornavn
                _bruger_obj.profil.mellemnavn = _mellemnavn if _mellemnavn != '' else _bruger_obj.profil.mellemnavn
                _bruger_obj.profil.efternavn = _efternavn if _efternavn != '' else _bruger_obj.profil.efternavn
                _bruger_obj.profil.save()

                if _adgangskode:
                    _user_obj = User.objects.get(username=_initialer)
                    _user_obj.set_password(_adgangskode)
                    _user_obj.save()

                _grupper = []
                for gruppe_obj in Gruppe.objects.all():
                    _grupper.append(gruppe_obj.navn)

                for _gruppe in _grupper:
                    _post_gruppe = request.POST[_gruppe] if _gruppe in request.POST else None

                    if _post_gruppe:
                        if not Gruppe.objects.filter(navn=_gruppe, bruger=_bruger_obj).first():
                            _gruppe_obj = Gruppe.objects.get(navn=_gruppe)
                            _gruppe_obj.bruger.add(_bruger_obj)

                    if not _post_gruppe:
                        _gruppe_obj = Gruppe.objects.filter(navn=_gruppe, bruger=_bruger_obj).first()
                        if _gruppe_obj:
                            _gruppe_obj.bruger.remove(_bruger_obj)

                messages.success(request, f"Brugeren '{_initialer}' blev oprettet.")
                return redirect('brugere_view')

        if not _initialer:
            messages.error(request, f"Udfyld venligst feltet 'Initialer'.")
            return render(request, 'system/bruger.html', {
                "bruger_rettigheder": list(rettigheder(request.user)),
                "initialer": _initialer,
                "fornavn": _fornavn,
                "mellemnavn": _mellemnavn,
                "efternavn": _efternavn,
                "adgangskode": '',
                "ny": True,
                "slet": False,
            })

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.db.models.functions import Lower
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
                _profil = Profil.objects.get(initialer=initialer)
                _bruger = Bruger.objects.get(profil=_profil)

                _tildelte_grupper = []
                for gruppe in Gruppe.objects.filter(bruger=_bruger).order_by(Lower('navn')):
                    _tildelte_grupper.append(gruppe.navn)

                return render(request, 'system/bruger.html', {
                    "bruger_rettigheder": list(rettigheder(request.user)),
                    "initialer": _bruger.profil.initialer,
                    "fornavn": _bruger.profil.fornavn,
                    "mellemnavn": _bruger.profil.mellemnavn,
                    "efternavn": _bruger.profil.efternavn,
                    "adgangskode": '',
                    "tildelte_grupper": _tildelte_grupper,
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

        _bruger = None

        if _initialer:
            if len(_initialer) != 3:
                messages.error(request, f"Initialer skal altid udgøres af tre tegn. Hverken mere eller mindre. Tre tegn!")
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

            if Profil.objects.filter(initialer=_initialer).exists():

                if 'slet' in request.POST:
                    messages.warning(request, f"Brugeren '{_initialer}' blev slettet.")

                    _user = User.objects.get(username=_initialer)
                    _profil = Profil.objects.get(initialer=_initialer)
                    _bruger = Bruger.objects.get(profil=_profil)

                    _user.delete()
                    _bruger.delete()
                    _profil.delete()

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
                    _profil = Profil.objects.get(initialer=_initialer)
                    _bruger = Bruger.objects.get(profil=_profil)

                    _bruger.profil.fornavn = _fornavn if _fornavn != '' else _bruger.profil.fornavn
                    _bruger.profil.mellemnavn = _mellemnavn if _mellemnavn != '' else _bruger.profil.mellemnavn
                    _bruger.profil.efternavn = _efternavn if _efternavn != '' else _bruger.profil.efternavn
                    _bruger.profil.save()

                    if _adgangskode != '':
                        _user = User.objects.get(username=_initialer)
                        _user.set_password(_adgangskode)
                        _user.save()

                    _grupper = []
                    for gruppe in Gruppe.objects.all().order_by(Lower('navn')):
                        _grupper.append(gruppe.navn)

                    for _g in _grupper:
                        _post_gruppe = request.POST[_g] if _g in request.POST else None
                        _gruppe = None

                        if _post_gruppe:
                            _gruppe = Gruppe.objects.filter(navn=_g, bruger=_bruger).first()
                            if not _gruppe:
                                _gruppe = Gruppe.objects.get(navn=_g)
                                _gruppe.bruger.add(_bruger)

                        if not _post_gruppe:
                            _gruppe = Gruppe.objects.filter(navn=_g, bruger=_bruger).first()
                            if _gruppe:
                                _gruppe.bruger.remove(_bruger)

                    messages.success(request, f"Brugeren '{_initialer}' blev gemt.")
                    return redirect('brugere_view')

            if not Profil.objects.filter(initialer=_initialer).exists():
                User.objects.create_user(username=_initialer)
                _profil = Profil.objects.create(initialer=_initialer)
                _bruger = Bruger.objects.create(profil=_profil)

                _bruger.profil.fornavn = _fornavn if _fornavn != '' else _bruger.profil.fornavn
                _bruger.profil.mellemnavn = _mellemnavn if _mellemnavn != '' else _bruger.profil.mellemnavn
                _bruger.profil.efternavn = _efternavn if _efternavn != '' else _bruger.profil.efternavn
                _bruger.profil.save()

                if _adgangskode:
                    _user = User.objects.get(username=_initialer)
                    _user.set_password(_adgangskode)
                    _user.save()

                _grupper = []
                for gruppe in Gruppe.objects.all().order_by(Lower('navn')):
                    _grupper.append(gruppe.navn)

                for _g in _grupper:
                    _post_gruppe = request.POST[_g] if _g in request.POST else None
                    _gruppe = None

                    if _post_gruppe:
                        _gruppe = Gruppe.objects.filter(navn=_g, bruger=_bruger).first()
                        if not _gruppe:
                            _gruppe = Gruppe.objects.get(navn=_g)
                            _gruppe.bruger.add(_bruger)

                    if not _post_gruppe:
                        _gruppe = Gruppe.objects.filter(navn=_g, bruger=_bruger).first()
                        if _gruppe:
                            _gruppe.bruger.remove(_bruger)

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

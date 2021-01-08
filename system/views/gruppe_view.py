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
                _gruppe = Gruppe.objects.get(navn=navn)

                _tildelte_rettigheder = []
                for rettighed in Gruppe.objects.get(navn=navn).rettighed_set.all():
                    _tildelte_rettigheder.append(rettighed.navn)

                return render(request, 'system/gruppe.html', {
                    "bruger_rettigheder": list(rettigheder(request.user)),
                    "navn": _gruppe.navn,
                    "tildelte_rettigheder": _tildelte_rettigheder,
                    "ny": False,
                    "slet": True,
                })

            if not Gruppe.objects.filter(navn=navn).exists():
                messages.error(request, "Den angivet gruppe findes ikke.")
                return redirect('grupper_view')

        if not navn:
            return render(request, 'system/gruppe.html', {
                "bruger_rettigheder": list(rettigheder(request.user)),
                "navn": '',
                "ny": True,
                "slet": False,
            })

    if request.method == 'POST' and tjek_rettigheder(request.user, {'system_gruppe_rediger'}):

        if 'fortryd' in request.POST:
            return redirect('grupper_view')

        _ny = request.POST['ny'] if 'ny' in request.POST else 'False'
        _navn = request.POST['navn'].upper().strip() if 'navn' in request.POST else None

        _gruppe = None

        if _navn:

            if Gruppe.objects.filter(navn=_navn).exists():

                if 'slet' in request.POST:
                    _gruppe = Gruppe.objects.get(navn=_navn)
                    _gruppe.delete()

                    messages.warning(request, f"Gruppen '{_navn}' blev slettet.")
                    return redirect('grupper_view')

                if _ny == 'True':
                    messages.error(request, f"Gruppen '{_navn}' findes allerede.")
                    return render(request, 'gruppe.html', {
                        "navn": _navn,
                        "ny": True,
                        "slet": False,
                        "bruger_rettigheder": list(rettigheder(request.user))
                    })

                if _ny == 'False':
                    _gruppe = Gruppe.objects.get(navn=_navn)
                    _gruppe.navn = _navn if _navn != '' else _gruppe.navn

                    _rettigheder = []
                    for rettighed in list(Rettighed._meta.get_field('navn').choices):
                        _rettigheder.append(rettighed[1])

                    for _r in _rettigheder:
                        _post_rettighed = request.POST[_r] if _r in request.POST else None
                        _rettighed = None

                        if _post_rettighed:
                            _rettighed = Rettighed.objects.filter(navn=_r, gruppe=_gruppe).first()
                            if not _rettighed:
                                Rettighed.objects.create(navn=_r, gruppe=_gruppe)

                        if not _post_rettighed:
                            _rettighed = Rettighed.objects.filter(navn=_r, gruppe=_gruppe).first()
                            if _rettighed:
                                _rettighed.delete()

                    _gruppe.save()

                    messages.success(request, f"Gruppen '{_navn}' blev gemt.")
                    return redirect('grupper_view')

            if not Gruppe.objects.filter(navn=_navn).exists():
                Gruppe.objects.create(navn=_navn)

                messages.success(request, f"Gruppen '{_navn}' blev oprettet.")
                return render(request, 'system/gruppe.html', {
                    "bruger_rettigheder": list(rettigheder(request.user)),
                    "navn": _navn,
                    "ny": False,
                    "slet": True,
                })

        if not _navn:
            messages.error(request, f"Udfyld venligst feltet 'Navn'.")
            return render(request, 'system/gruppe.html', {
                "bruger_rettigheder": list(rettigheder(request.user)),
                "navn": _navn,
                "ny": True,
                "slet": False,
            })

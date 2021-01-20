from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from hardware.models import Medie
from system.services import rettigheder, tjek_rettigheder


def tjek(user):
    return tjek_rettigheder(user, {'hardware_medie_se'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def medie_view(request, pk=None):

    if request.method == 'GET':

        if pk:
            if Medie.objects.filter(pk=pk).exists():
                _medie_obj = Medie.objects.get(pk=pk)

                return render(request, 'hardware/medie.html', {
                    "bruger_rettigheder": rettigheder(request.user),
                    "pk": _medie_obj.pk,
                    "navn": _medie_obj.navn,
                    "producent": _medie_obj.producent,
                    "kapacitet": _medie_obj.kapacitet,
                    "medie_type": _medie_obj.type,
                    "ny": False,
                })

            if not Medie.objects.filter(pk=pk).exists():
                messages.error(request, "Det angivet medie findes ikke.")
                return redirect('medier_view')

        if not pk:
            messages.error(request, "Intet medie angivet.")
            return redirect('medier_view')

    if request.method == 'POST' and tjek_rettigheder(request.user, {'hardware_medie_rediger'}):

        if 'fortryd' in request.POST:
            return redirect('medier_view')

        _pk = request.POST['pk'] if 'pk' in request.POST else None
        _navn = request.POST['navn'].upper() if 'navn' in request.POST else None
        _producent = request.POST['producent'] if 'producent' in request.POST else None
        _kapacitet = request.POST['kapacitet'] if 'kapacitet' in request.POST else None
        _medie_type = request.POST['medie_type'] if 'medie_type' in request.POST else None

        if _pk:
            _medie_obj = None
            _tjek_navn = False
            _tjek_kapacitet = False

            try:
                _pk = int(_pk)
            except ValueError:
                messages.error(request, f"Det angivet medie findes ikke.")
                return redirect('medier_view')

            if Medie.objects.filter(pk=_pk).exists():
                _medie_obj = Medie.objects.get(pk=_pk)
            else:
                messages.error(request, f"Det angivet medie findes ikke.")
                return redirect('medier_view')

            if 'slet' in request.POST and tjek_rettigheder(request.user, {'hardware_medie_slet'}):
                messages.warning(request, f"Mediet '{_medie_obj.navn}' blev slettet.")
                _medie_obj.delete()
                return redirect('medier_view')

            if _navn != '' and Medie.objects.filter(navn=_navn).exists():
                _navn_medie_obj = Medie.objects.filter(navn=_navn).first()
                if _medie_obj.pk == _navn_medie_obj.pk:
                    _tjek_navn = True
                else:
                    _tjek_navn = False
                    messages.error(request, f"Et medie med navnet '{_navn}' findes allerede.")
            else:
                _tjek_navn = True

            if _kapacitet != '':
                try:
                    _kapacitet = int(_kapacitet)
                    _tjek_kapacitet = True
                except ValueError:
                    _tjek_kapacitet = False
                    messages.error(request, "'Kapacitet i GB' er ikke et heltal.")
            else:
                _kapacitet = 0
                _tjek_kapacitet = True

            if not _tjek_navn or not _tjek_kapacitet:
                return render(request, 'hardware/medie.html', {
                    "bruger_rettigheder": rettigheder(request.user),
                    "pk": _pk,
                    "navn": _navn,
                    "producent": _producent,
                    "kapacitet": _kapacitet,
                    "medie_type": _medie_type,
                    "ny": False,
                })

            _medie_obj.navn = _navn.strip()
            _medie_obj.producent = _producent.strip()
            _medie_obj.kapacitet = _kapacitet
            _medie_obj.type = _medie_type
            _medie_obj.save()

            messages.success(request, f"Mediet '{_medie_obj.navn}' blev gemt.")
            return redirect('medier_view')

        if not _pk and tjek_rettigheder(request.user, {'hardware_medie_opret'}):
            _medie_obj = Medie.objects.create()
            messages.success(request, "Nyt medie blev oprettet.")
            return render(request, 'hardware/medie.html', {
                "bruger_rettigheder": rettigheder(request.user),
                "pk": _medie_obj.pk,
                "navn": _medie_obj.navn,
                "producent": _medie_obj.producent,
                "kapacitet": _medie_obj.kapacitet,
                "medie_type": _medie_obj.type,
                "ny": True,
            })

        return redirect('medier_view')

    return redirect('medier_view')

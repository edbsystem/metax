from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from arkiveringsversioner.models import Leverandoer
from system.services import rettigheder, tjek_rettigheder


def tjek(user):
    return tjek_rettigheder(user, {'arkiveringsversioner_leverandør_se'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def leverandoer_view(request, pk=None):

    if request.method == 'GET':

        print('request.GET:', request.GET)

        if pk:
            if Leverandoer.objects.filter(pk=pk).exists():
                _leverandoer_obj = Leverandoer.objects.get(pk=pk)

                return render(request, 'arkiveringsversioner/leverandoer.html', {
                    "bruger_rettigheder": rettigheder(request.user),
                    "pk": _leverandoer_obj.pk,
                    "navn": _leverandoer_obj.navn,
                })

            if not Leverandoer.objects.filter(pk=pk).exists():
                messages.error(request, "Den angivet leverandør findes ikke.")
                return redirect('leverandoerer_view')

        if not pk:
            messages.error(request, "Ingen leverandør angivet.")
            return redirect('leverandoerer_view')

    if request.method == 'POST' and tjek_rettigheder(request.user, {'arkiveringsversioner_leverandør_rediger'}):

        print('request.POST:', request.POST)

        if 'fortryd' in request.POST:
            return redirect('leverandoerer_view')

        _pk = request.POST['pk'] if 'pk' in request.POST else None
        _navn = request.POST['navn'] if 'navn' in request.POST else None

        if _pk:
            _leverandoer_obj = None
            _tjek_navn = False

            try:
                _pk = int(_pk)
            except ValueError:
                messages.error(request, f"Den angivet leverandør findes ikke.")
                return redirect('leverandoerer_view')

            if Leverandoer.objects.filter(pk=_pk).exists():
                _leverandoer_obj = Leverandoer.objects.get(pk=_pk)
            else:
                messages.error(request, f"Den angivet leverandør findes ikke.")
                return redirect('leverandoerer_view')

            print('slet:', request.POST)

            if 'slet' in request.POST and tjek_rettigheder(request.user, {'arkiveringsversioner_leverandør_slet'}):
                messages.warning(request, f"Leverandøren '{_leverandoer_obj.navn}' blev slettet.")
                _leverandoer_obj.delete()
                return redirect('leverandoerer_view')

            if _navn != '' and Leverandoer.objects.filter(navn=_navn).exists():
                _navn_leverandoer_obj = Leverandoer.objects.filter(navn=_navn).first()
                if _leverandoer_obj.pk == _navn_leverandoer_obj.pk:
                    _tjek_navn = True
                else:
                    _tjek_navn = False
                    messages.error(request, f"En leverandør med navnet '{_navn}' findes allerede.")
            else:
                _tjek_navn = True

            if not _tjek_navn:
                return render(request, 'arkiveringsversioner/leverandoer.html', {
                    "bruger_rettigheder": rettigheder(request.user),
                    "pk": _pk,
                    "navn": _navn,
                })

            _leverandoer_obj.navn = _navn.strip()
            _leverandoer_obj.save()

            messages.success(request, f"Leverandøren '{_leverandoer_obj.navn}' blev gemt.")
            return redirect('leverandoerer_view')

        if not _pk and tjek_rettigheder(request.user, {'arkiveringsversioner_leverandør_opret'}):
            _leverandoer_obj = Leverandoer.objects.create()
            messages.success(request, "Ny leverandør blev oprettet.")
            return render(request, 'arkiveringsversioner/leverandoer.html', {
                "bruger_rettigheder": rettigheder(request.user),
                "pk": _leverandoer_obj.pk,
                "navn": _leverandoer_obj.navn,
                "ny": True,
            })

        return redirect('leverandoerer_view')

    return redirect('leverandoerer_view')

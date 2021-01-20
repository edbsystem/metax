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

        if pk:
            if Leverandoer.objects.filter(pk=pk).exists():
                _leverandoer_obj = Leverandoer.objects.get(pk=pk)

                return render(request, 'arkiveringsversioner/leverandoer.html', {
                    "bruger_rettigheder": rettigheder(request.user),
                    "pk": _leverandoer_obj.pk,
                    "navn": _leverandoer_obj.navn,
                    "ny": False,
                })

            if not Leverandoer.objects.filter(pk=pk).exists():
                messages.error(request, "Den angivet leverandør findes ikke.")
                return redirect('leverandoerer_view')

        if not pk:
            messages.error(request, "Ingen leverandør angivet.")
            return redirect('leverandoerer_view')

    if request.method == 'POST' and tjek_rettigheder(request.user, {'arkiveringsversioner_leverandør_rediger'}):
        pass

    return redirect('leverandoerer_view')

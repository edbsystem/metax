from hardware.models.medie import Medie
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from system.services import rettigheder, tjek_rettigheder
from arkiveringsversioner.models import Arkiveringsversion, Version
from hardware.models import Maskine


def tjek(user):
    return tjek_rettigheder(user, {'arkiveringsversioner_se'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def views_view(request, view=None):

    if not view:
        messages.error(request, "Angiv venligst et legalt view.")
        return redirect('forside_view')

    if view:

        if view == 'frie_maskiner':
            pass

        if view == 'afvikler_ada':
            pass

        if view == 'forhaandsgodkendt':
            pass

        if view == 'send_til_dea':
            pass

        if view == 'parat_til_test':
            pass

        if view == 'under_test':
            pass

        # return render(request, 'arkiveringsversioner/views_view.html', {
        #     "bruger_rettigheder": rettigheder(request.user),
        # })

        messages.error(request, "Det angivet view er ikke legalt.")
        return redirect('forside_view')

    return redirect('forside_view')

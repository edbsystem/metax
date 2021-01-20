from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

from system.services import rettigheder, tjek_rettigheder


def tjek(user):
    return tjek_rettigheder(user, {'arkiveringsversioner_typer_se'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def typer_view(request):
    return render(request, 'arkiveringsversioner/typer.html', {
        "bruger_rettigheder": rettigheder(request.user),
    })

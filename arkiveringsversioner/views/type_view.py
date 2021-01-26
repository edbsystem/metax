from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from arkiveringsversioner.models import Type
from system.services import rettigheder, tjek_rettigheder


def tjek(user):
    return tjek_rettigheder(user, {'arkiveringsversioner_type_se'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def type_view(request, pk=None):

    if request.method == 'GET':

        if pk:
            if Type.objects.filter(pk=pk).exists():
                _type_obj = Type.objects.get(pk=pk)

                return render(request, 'arkiveringsversioner/type.html', {
                    "bruger_rettigheder": rettigheder(request.user),
                    "pk": _type_obj.pk,
                    "navn": _type_obj.navn,
                })

            if not Type.objects.filter(pk=pk).exists():
                messages.error(request, "Den angivet type findes ikke.")
                return redirect('typer_view')

        if not pk:
            messages.error(request, "Ingen type angivet.")
            return redirect('typer_view')

    if request.method == 'POST' and tjek_rettigheder(request.user, {'arkiveringsversioner_type_rediger'}):

        if 'fortryd' in request.POST:
            return redirect('typer_view')

        _pk = request.POST['pk'] if 'pk' in request.POST else None
        _navn = request.POST['navn'] if 'navn' in request.POST else None

        if _pk:
            _type_obj = None
            _tjek_navn = False

            try:
                _pk = int(_pk)
            except ValueError:
                messages.error(request, f"Den angivet type findes ikke.")
                return redirect('typer_view')

            if Type.objects.filter(pk=_pk).exists():
                _type_obj = Type.objects.get(pk=_pk)
            else:
                messages.error(request, f"Den angivet type findes ikke.")
                return redirect('typer_view')

            if 'slet' in request.POST and tjek_rettigheder(request.user, {'arkiveringsversioner_type_slet'}):
                messages.warning(request, f"Type '{_type_obj.navn}' blev slettet.")
                _type_obj.delete()
                return redirect('typer_view')

            if _navn != '' and Type.objects.filter(navn=_navn).exists():
                _navn_type_obj = Type.objects.filter(navn=_navn).first()
                if _type_obj.pk == _navn_type_obj.pk:
                    _tjek_navn = True
                else:
                    _tjek_navn = False
                    messages.error(request, f"En type med navnet '{_navn}' findes allerede.")
            else:
                _tjek_navn = True

            if not _tjek_navn:
                return render(request, 'arkiveringsversioner/type.html', {
                    "bruger_rettigheder": rettigheder(request.user),
                    "pk": _pk,
                    "navn": _navn,
                })

            _type_obj.navn = _navn.strip()
            _type_obj.save()

            messages.success(request, f"Typen '{_type_obj.navn}' blev gemt.")
            return redirect('typer_view')

        if not _pk and tjek_rettigheder(request.user, {'arkiveringsversioner_type_opret'}):
            _type_obj = Type.objects.create()
            messages.success(request, "Ny type blev oprettet.")
            return render(request, 'arkiveringsversioner/type.html', {
                "bruger_rettigheder": rettigheder(request.user),
                "pk": _type_obj.pk,
                "navn": _type_obj.navn,
                "ny": True,
            })

        return redirect('typer_view')

    return redirect('typer_view')

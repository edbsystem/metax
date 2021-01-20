from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from hardware.models import Maskine, Placering
from system.services import rettigheder, tjek_rettigheder


def tjek(user):
    return tjek_rettigheder(user, {'hardware_maskine_se'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def maskine_view(request, pk=None):

    if request.method == 'GET':

        if pk:
            if Maskine.objects.filter(pk=pk).exists():
                _maskine = Maskine.objects.get(pk=pk)

                return render(request, 'hardware/maskine.html', {
                    "bruger_rettigheder": rettigheder(request.user),
                    "pk": _maskine.pk,
                    "navn": _maskine.navn,
                    "processor": _maskine.processor,
                    "bundkort": _maskine.bundkort,
                    "arbejdshukommelse": _maskine.arbejdshukommelse,
                    "maskine_type": _maskine.type,
                    "lokation": _maskine.placering.lokation if _maskine.placering else None,
                    "lokale": _maskine.placering.lokale if _maskine.placering else None,
                    "netvaerk": _maskine.placering.netvaerk if _maskine.placering else None,
                    "kommentar": _maskine.kommentar,
                    "ny": False,
                })
            else:
                messages.error(request, "Den angivet maskine findes ikke.")
                return redirect('maskiner_view')

        if not pk:
            messages.error(request, "Ingen maskine angivet.")
            return redirect('maskiner_view')

    if request.method == 'POST' and tjek_rettigheder(request.user, {'hardware_maskine_rediger'}):

        if 'fortryd' in request.POST:
            return redirect('maskiner_view')

        _pk = request.POST['pk'] if 'pk' in request.POST else None
        _navn = request.POST['navn'].upper() if 'navn' in request.POST else None
        _processor = request.POST['processor'] if 'processor' in request.POST else None
        _bundkort = request.POST['bundkort'] if 'bundkort' in request.POST else None
        _arbejdshukommelse = request.POST['arbejdshukommelse'] if 'arbejdshukommelse' in request.POST else None
        _type = request.POST['maskine_type'] if 'maskine_type' in request.POST else None
        _lokation = request.POST['lokation'] if 'lokation' in request.POST else None
        _lokale = request.POST['lokale'] if 'lokale' in request.POST else None
        _netvaerk = request.POST['netvaerk'] if 'netvaerk' in request.POST else None
        _kommentar = request.POST.get('kommentar') if request.POST.get('kommentar') else ''

        if _pk:
            _maskine = None
            _tjek_navn = False
            _tjek_arbejdshukommelse = False

            try:
                _pk = int(_pk)
            except ValueError:
                messages.error(request, f"Den angivet maskine findes ikke.")
                return redirect('maskiner_view')

            if Maskine.objects.filter(pk=_pk).exists():
                _maskine = Maskine.objects.get(pk=_pk)
            else:
                messages.error(request, f"Den angivet maskine findes ikke.")
                return redirect('maskiner_view')

            if 'slet' in request.POST and tjek_rettigheder(request.user, {'hardware_maskine_slet'}):
                messages.warning(request, f"Maskinen '{_maskine.navn}' blev slettet.")
                _maskine.placering.delete()
                _maskine.delete()
                return redirect('maskiner_view')

            if _navn != '' and Maskine.objects.filter(navn=_navn).exists():
                _navn_maskine = Maskine.objects.filter(navn=_navn).first()
                if _maskine.pk == _navn_maskine.pk:
                    _tjek_navn = True
                else:
                    _tjek_navn = False
                    messages.error(request, f"En maskine med navnet '{_navn}' findes allerede.")
            else:
                _tjek_navn = True

            if _arbejdshukommelse != '':
                try:
                    _arbejdshukommelse = int(_arbejdshukommelse)
                    _tjek_arbejdshukommelse = True
                except ValueError:
                    _tjek_arbejdshukommelse = False
                    messages.error(request, "'Arbejdshukommelse i GB' er ikke et heltal.")
            else:
                _arbejdshukommelse = 0
                _tjek_arbejdshukommelse = True

            if not _tjek_navn or not _tjek_arbejdshukommelse:
                return render(request, 'hardware/maskine.html', {
                    "bruger_rettigheder": rettigheder(request.user),
                    "pk": _pk,
                    "navn": _navn,
                    "processor": _processor,
                    "bundkort": _bundkort,
                    "arbejdshukommelse": _arbejdshukommelse,
                    "type": _type,
                    "lokation": _lokation,
                    "lokale": _lokale,
                    "netvaerk": _netvaerk,
                    "kommentar": _kommentar,
                    "ny": False,
                })

            _maskine.navn = _navn.strip()
            _maskine.processor = _processor.strip()
            _maskine.bundkort = _bundkort.strip()
            _maskine.arbejdshukommelse = _arbejdshukommelse
            _maskine.type = _type
            _maskine.placering.lokation = _lokation
            _maskine.placering.lokale = _lokale
            _maskine.placering.netvaerk = _netvaerk
            _maskine.placering.save()
            _maskine.kommentar = _kommentar
            _maskine.save()

            messages.success(request, f"Maskinen '{_maskine.navn}' blev gemt.")
            return redirect('maskiner_view')

        if not _pk and tjek_rettigheder(request.user, {'hardware_maskine_opret'}):
            _maskine = Maskine.objects.create(placering=Placering.objects.create())

            messages.success(request, "Ny maskine blev oprettet.")
            return render(request, 'hardware/maskine.html', {
                "bruger_rettigheder": rettigheder(request.user),
                "pk": _maskine.pk,
                "navn": _maskine.navn,
                "processor": _maskine.processor,
                "bundkort": _maskine.bundkort,
                "arbejdshukommelse": _maskine.arbejdshukommelse,
                "type": _maskine.type,
                "lokation": _maskine.placering.lokation if _maskine.placering else None,
                "lokale": _maskine.placering.lokale if _maskine.placering else None,
                "netvaerk": _maskine.placering.netvaerk if _maskine.placering else None,
                "kommentar": _maskine.kommentar,
                "ny": True,
            })

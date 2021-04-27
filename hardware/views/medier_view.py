from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models.functions import Lower

from hardware.models import Medie
from system.services import rettigheder, tjek_rettigheder


def tjek(user):
    return tjek_rettigheder(user, {'hardware_medier_se'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def medier_view(request):

    _medier_objs = sorted(Medie.objects.all(), key=lambda _medie: _medie.navn)

    _medier = []
    for _medie_obj in _medier_objs:
        versioner_objs = _medie_obj.versioner.all()
        versioner = []
        for v in versioner_objs:
            versioner.append(v.avid.avid)
        _medier.append({
            "pk": _medie_obj.pk,
            "navn": _medie_obj.navn,
            "producent": _medie_obj.producent,
            "kapacitet": _medie_obj.kapacitet,
            "versioner": versioner,
            "maskine": _medie_obj.maskine,
        })

    print(_medier)

    return render(request, 'hardware/medier.html', {
        "bruger_rettigheder": rettigheder(request.user),
        "medier": _medier,
    })

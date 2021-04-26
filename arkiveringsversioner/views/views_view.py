from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from datetime import datetime

from system.services import rettigheder, tjek_rettigheder
from arkiveringsversioner.models import Arkiveringsversion, Type, Version, Leverandoer, leverandoer
from system.models import Bruger, Profil


def tjek(user):
    return tjek_rettigheder(user, {'arkiveringsversioner_se'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def views_view(request, view):
    versioner = []

    if view == 'mangler_maskine':
        versioner_objs = Version.objects.filter(status='Modtaget').order_by('svarfrist')

        for version_obj in versioner_objs:
            av_obj = Arkiveringsversion.objects.filter(avid=version_obj.avid.avid).first()
            versioner.append({
                "avid": av_obj.avid,
                "jnr": av_obj.jnr,
                "titel": av_obj.titel,
                "kategori": av_obj.kategori,
                "svarfrist": '{:%d-%m-%Y}'.format(version_obj.svarfrist) if version_obj.svarfrist != None else '',
            })

        print(versioner)

    return render(request, 'arkiveringsversioner/mangler_maskine.html', {
        "bruger_rettigheder": rettigheder(request.user),
        "versioner": versioner,
    })

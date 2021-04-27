from hardware.models.medie import Medie
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from datetime import datetime

from system.services import rettigheder, tjek_rettigheder
from arkiveringsversioner.models import Arkiveringsversion, Version
from hardware.models import Maskine


def tjek(user):
    return tjek_rettigheder(user, {'arkiveringsversioner_se'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def mangler_maskine_view(request, maskine=None, avid=None, version=None):

    if not maskine or not avid or not version:

        versioner = []
        stoerrelse = 0

        versioner_objs = Version.objects.filter(
            status='Modtaget',
            modtaget_kopieret=True,
            modtaget_modtagelse_godkendt=True,

        ).order_by('svarfrist')

        for version_obj in versioner_objs:
            av_obj = Arkiveringsversion.objects.filter(avid=version_obj.avid.avid).first()
            if len(Medie.objects.filter(versioner=version_obj, maskine=None)) > 0:
                if Medie.objects.filter(maskine=None):
                    versioner.append({
                        "avid": av_obj.avid,
                        "version": version_obj.nummer,
                        "jnr": av_obj.jnr,
                        "titel": av_obj.titel,
                        "kategori": av_obj.kategori,
                        "svarfrist": '{:%d-%m-%Y}'.format(version_obj.svarfrist) if version_obj.svarfrist != None else '',
                        "stoerrelse": int(version_obj.stoerrelsemb / 1024),
                    })
                    stoerrelse += version_obj.stoerrelsemb

        return render(request, 'arkiveringsversioner/mangler_maskine.html', {
            "bruger_rettigheder": rettigheder(request.user),
            "versioner": versioner,
            "samlet_stoerrelse": int(stoerrelse / 1024),
        })

    if maskine or avid or version:

        _maskine_obj = Maskine.objects.get(navn=maskine)
        _arkiveringsversion_obj = Arkiveringsversion.objects.get(avid=avid)
        _version_obj = Version.objects.get(nummer=version, avid=_arkiveringsversion_obj)
        _medie_obj = Medie.objects.filter(versioner=_version_obj).first()
        _medie_obj.maskine = _maskine_obj
        _medie_obj.save()
        messages.success(request, f"Maskinen '{_maskine_obj.navn}' tildelt til version '{_version_obj.nummer}' af 'AVID.{_version_obj.avid}'")

    return redirect('arkiveringsversion_view', avid=avid, version=version)

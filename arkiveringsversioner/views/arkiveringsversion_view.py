from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from system.services import rettigheder, tjek_rettigheder
from arkiveringsversioner.models import Arkiveringsversion, Version


def tjek(user):
    return tjek_rettigheder(user, {'arkiveringsversioner_arkiveringsversion_se'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def arkiveringsversion_view(request, avid, version=0):

    try:
        _avid = int(avid)
    except ValueError:
        messages.error(request, f"Det angivet AVID: '{avid}', overholder ikke reglerne for et sådant.")
        return redirect('arkiveringsversioner_view')

    try:
        _version = int(version)
    except ValueError:
        messages.error(request, f"Den angivet version: '{version}', overholder ikke reglerne for et sådant.")
        return redirect('arkiveringsversioner_view')

    if request.method == 'GET':

        _arkiveringsversion_obj = None
        _version_obj = None

        if Arkiveringsversion.objects.filter(avid=avid).exists():
            _arkiveringsversion_obj = Arkiveringsversion.objects.get(avid=avid)

            version = version if version != 0 else Version.objects.filter(avid=_arkiveringsversion_obj).count()

            if Version.objects.filter(nummer=version, avid=_arkiveringsversion_obj).exists():
                _version_obj = Version.objects.get(nummer=version, avid=_arkiveringsversion_obj)

            if not Version.objects.filter(nummer=version, avid=_arkiveringsversion_obj).exists():
                messages.error(request, f"Den angivet version af arkiveringsversionen 'AVID.SA.{avid}' findes ikke.")
                return redirect('arkiveringsversioner_view')

            _tester_fuldenavn = ''
            if _version_obj.tester.profil.fornavn != '' and _version_obj.tester.profil.fornavn != None:
                _tester_fuldenavn += _version_obj.tester.profil.fornavn
            if _version_obj.tester.profil.mellemnavn != '' and _version_obj.tester.profil.mellemnavn != None:
                _tester_fuldenavn += ' '
                _tester_fuldenavn += _version_obj.tester.profil.mellemnavn
            if _version_obj.tester.profil.efternavn != '' and _version_obj.tester.profil.efternavn != None:
                _tester_fuldenavn += ' '
                _tester_fuldenavn += _version_obj.tester.profil.efternavn

            _arkivar_fuldenavn = ''
            if _version_obj.arkivar.profil.fornavn != '' and _version_obj.arkivar.profil.fornavn != None:
                _arkivar_fuldenavn += _version_obj.arkivar.profil.fornavn
            if _version_obj.arkivar.profil.mellemnavn != '' and _version_obj.arkivar.profil.mellemnavn != None:
                _arkivar_fuldenavn += ' '
                _arkivar_fuldenavn += _version_obj.arkivar.profil.mellemnavn
            if _version_obj.arkivar.profil.efternavn != '' and _version_obj.arkivar.profil.efternavn != None:
                _arkivar_fuldenavn += ' '
                _arkivar_fuldenavn += _version_obj.arkivar.profil.efternavn

            print("modtaget_kvitteret", _version_obj.modtaget_kvitteret)
            print("modtaget_journaliseret", _version_obj.modtaget_journaliseret)
            print("modtaget_kodeord", _version_obj.modtaget_kodeord)
            print("modtaget_mangler_kodeord", _version_obj.modtaget_mangler_kodeord)
            print("modtaget_ikke_krypteret", _version_obj.modtaget_ikke_krypteret)
            print("modtaget_kopieret", _version_obj.modtaget_kopieret)
            print("modtaget_modtagelse_godkendt", _version_obj.modtaget_modtagelse_godkendt)
            print("modtaget_modtagelse_afvist", _version_obj.modtaget_modtagelse_afvist)
            print("modtaget_fileindex_kopieret", _version_obj.modtaget_fileindex_kopieret)
            print("modtaget_adatest_godkendt", _version_obj.modtaget_adatest_godkendt)
            print("modtaget_adatest_afvist", _version_obj.modtaget_adatest_afvist)
            print("tilbagemeldt_nedpakket", _version_obj.tilbagemeldt_nedpakket)
            print("tilbagemeldt_maskine_renset", _version_obj.tilbagemeldt_maskine_renset)
            print("godkendt_af_tester_fileindex_godkendt", _version_obj.godkendt_af_tester_fileindex_godkendt)
            print("godkendt_af_tester_afvikler_dea", _version_obj.godkendt_af_tester_afvikler_dea)
            print("godkendt_af_tester_afleveret_til_dea", _version_obj.godkendt_af_tester_afleveret_til_dea)
            print("godkendt_af_tester_retur_fra_dea", _version_obj.godkendt_af_tester_retur_fra_dea)
            print("godkendt_af_tester_mary_kontrol", _version_obj.godkendt_af_tester_mary_kontrol)
            print("godkendt_af_tester_meta_opdateret", _version_obj.godkendt_af_tester_meta_opdateret)
            print("godkendt_af_tester_public_opdateret", _version_obj.godkendt_af_tester_public_opdateret)
            print("godkendt_af_tester_nedpakket", _version_obj.godkendt_af_tester_nedpakket)
            print("godkendt_af_tester_maskine_renset", _version_obj.godkendt_af_tester_maskine_renset)

            return render(request, 'arkiveringsversioner/arkiveringsversion.html', {
                "bruger_rettigheder": rettigheder(request.user),
                "avid": _arkiveringsversion_obj.avid,
                "jnr": _arkiveringsversion_obj.jnr,
                "public": _arkiveringsversion_obj.public,
                "titel": _arkiveringsversion_obj.titel,
                "kategori": _arkiveringsversion_obj.kategori,
                "klassifikation": _arkiveringsversion_obj.klassifikation,
                "type": str(_arkiveringsversion_obj.type),
                "land": _arkiveringsversion_obj.land,
                "noterfraarkivar": _arkiveringsversion_obj.arkivar_noter,
                "noterfratester": _arkiveringsversion_obj.tester_noter,
                "versioner": [''] * Version.objects.filter(avid=_arkiveringsversion_obj).count(),
                "version": int(version),
                "tester": _tester_fuldenavn,
                "arkivar": _arkivar_fuldenavn,
                "leverandoer": str(_version_obj.leverandoer),
                "stoerrelsemb": _version_obj.stoerrelsemb,
                "stoerrelsegb": int(_version_obj.stoerrelsemb / 1024),
                "afleveringsfrist": '{:%d-%m-%Y}'.format(_version_obj.afleveringsfrist) if _version_obj.afleveringsfrist != None else '',
                "modtaget": '{:%d-%m-%Y}'.format(_version_obj.modtaget) if _version_obj.modtaget != None else '',
                "adgang": '{:%d-%m-%Y}'.format(_version_obj.adgang) if _version_obj.adgang != None else '',
                "svarfrist": '{:%d-%m-%Y}'.format(_version_obj.svarfrist) if _version_obj.svarfrist != None else '',
                "svar": '{:%d-%m-%Y}'.format(_version_obj.svar) if _version_obj.svar != None else '',
                "status": _version_obj.status,
                "modtaget_kvitteret": _version_obj.modtaget_kvitteret,
                "modtaget_journaliseret": _version_obj.modtaget_journaliseret,
                "modtaget_kodeord": _version_obj.modtaget_kodeord,
                "modtaget_mangler_kodeord": _version_obj.modtaget_mangler_kodeord,
                "modtaget_ikke_krypteret": _version_obj.modtaget_ikke_krypteret,
                "modtaget_kopieret": _version_obj.modtaget_kopieret,
                "modtaget_modtagelse_godkendt": _version_obj.modtaget_modtagelse_godkendt,
                "modtaget_modtagelse_afvist": _version_obj.modtaget_modtagelse_afvist,
                "modtaget_fileindex_kopieret": _version_obj.modtaget_fileindex_kopieret,
                "modtaget_adatest_godkendt": _version_obj.modtaget_adatest_godkendt,
                "modtaget_adatest_afvist": _version_obj.modtaget_adatest_afvist,
                "tilbagemeldt_nedpakket": _version_obj.tilbagemeldt_nedpakket,
                "tilbagemeldt_maskine_renset": _version_obj.tilbagemeldt_maskine_renset,
                "godkendt_af_tester_fileindex_godkendt": _version_obj.godkendt_af_tester_fileindex_godkendt,
                "godkendt_af_tester_afvikler_dea": _version_obj.godkendt_af_tester_afvikler_dea,
                "godkendt_af_tester_afleveret_til_dea": _version_obj.godkendt_af_tester_afleveret_til_dea,
                "godkendt_af_tester_retur_fra_dea": _version_obj.godkendt_af_tester_retur_fra_dea,
                "godkendt_af_tester_mary_kontrol": _version_obj.godkendt_af_tester_mary_kontrol,
                "godkendt_af_tester_meta_opdateret": _version_obj.godkendt_af_tester_meta_opdateret,
                "godkendt_af_tester_public_opdateret": _version_obj.godkendt_af_tester_public_opdateret,
                "godkendt_af_tester_nedpakket": _version_obj.godkendt_af_tester_nedpakket,
                "godkendt_af_tester_maskine_renset": _version_obj.godkendt_af_tester_maskine_renset,
            })

        if not Arkiveringsversion.objects.filter(avid=avid).exists():
            messages.error(request, "Den angivet arkiveringsversion findes ikke.")
            return redirect('arkiveringsversioner_view')

    if request.method == 'POST':
        print('kvitteret:', request.POST.get('kvitteret'))
        print('journaliseret', request.POST.get('journaliseret'))
        print('kodeord:', request.POST.get('kodeord'))
        print('kopieret:', request.POST.get('kopieret'))
        return redirect('/arkiveringsversioner/arkiveringsversion/18000/2/')

    return render(request, 'arkiveringsversioner/arkiveringsversioner.html', {
        "bruger_rettigheder": rettigheder(request.user),
    })

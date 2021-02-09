from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from datetime import datetime

from system.services import rettigheder, tjek_rettigheder
from arkiveringsversioner.models import Arkiveringsversion, Version


def tjek(user):
    return tjek_rettigheder(user, {'arkiveringsversioner_arkiveringsversion_se'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def arkiveringsversion_view(request, avid, version=0, nystatus=None):

    _url_error = False

    try:
        _avid = int(avid)
    except ValueError:
        messages.error(request, f"Det angivet AVID: '{avid}', overholder ikke reglerne for et sådant.")
        _url_error = True

    try:
        _version = int(version)
    except ValueError:
        messages.error(request, f"Den angivet version: '{version}', overholder ikke reglerne for et sådant.")
        _url_error = True

    _statusser = ['modtaget', 'klar_til_test', 'tilbagemeldt', 'begynd_test', 'godkendt_af_tester', 'afvent_genaflevering', 'parat_til_godkendelse', 'godkendt']
    _nystatus = {nystatus}

    if nystatus != None and not _nystatus.issubset(_statusser):
        messages.error(request, f"Den angivet status: '{nystatus}', er ikke kendt.")
        _url_error = True

    if _url_error:
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

            _status_error = False
            _ny_status = None

            if nystatus != None:
                if _version_obj.status == 'Afventer aflevering':
                    if nystatus != 'modtaget':
                        _status_error = True
                    else:
                        _ny_status = 'Modtaget'
                if _version_obj.status == 'Modtaget':
                    if nystatus != 'klar_til_test' and nystatus != 'tilbagemeldt':
                        _status_error = True
                    else:
                        if nystatus == 'klar_til_test':
                            _ny_status = 'Klar til test'
                        if nystatus == 'tilbagemeldt':
                            _ny_status = 'Tilbagemeldt'
                if _version_obj.status == 'Klar til test':
                    if nystatus != 'begynd_test':
                        _status_error = True
                    else:
                        _ny_status = 'Under test'
                if _version_obj.status == 'Under test':
                    if nystatus != 'tilbagemeldt' and nystatus != 'godkendt_af_tester':
                        _status_error = True
                    else:
                        if nystatus == 'tilbagemeldt':
                            _ny_status = 'Tilbagemeldt'
                        if nystatus == 'godkendt_af_tester':
                            _ny_status = 'Godkendt af tester'
                if _version_obj.status == 'Tilbagemeldt':
                    if nystatus != 'afvent_genaflevering':
                        _status_error = True
                    else:
                        _ny_status = 'Afventer genaflevering'
                if _version_obj.status == 'Afventer genaflevering':
                    if nystatus != 'modtaget':
                        _status_error = True
                    else:
                        _ny_status = 'Modtaget'
                if _version_obj.status == 'Godkendt af tester':
                    if nystatus != 'parat_til_godkendelse':
                        _status_error = True
                    else:
                        _ny_status = 'Parat til godkendelse'
                if _version_obj.status == 'Parat til godkendelse':
                    if nystatus != 'godkendt':
                        _status_error = True
                    else:
                        _ny_status = 'Godkendt'

            if _status_error:
                messages.error(request, f"Det angivet statusskift er ikke tilladt.")
                return redirect(f"/arkiveringsversioner/arkiveringsversion/{avid}/{version}/")

            if _ny_status:
                _gammel_status = _version_obj.status
                _version_obj.status = _ny_status
                _version_obj.save()
                # messages.success(request, f"Status skiftet fra '{_gammel_status}' til '{_ny_status}'.")
                return redirect(f"/arkiveringsversioner/arkiveringsversion/{avid}/{version}/")

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
                "godkendt_af_tester_maskine_renset": _version_obj.godkendt_af_tester_maskine_renset,
                "dagsdato": datetime.today().strftime('%d-%m-%Y'),
            })

        if not Arkiveringsversion.objects.filter(avid=avid).exists():
            messages.error(request, "Den angivet arkiveringsversion findes ikke.")
            return redirect('arkiveringsversioner_view')

    if request.method == 'POST':

        _avid = request.POST.get('avid')
        _jnr = request.POST.get('jnr')
        _public_link = request.POST.get('public_link')
        _titel = request.POST.get('titel')
        _kategori = request.POST.get('kategori')
        _klassifikation = request.POST.get('klassifikation')
        _type = request.POST.get('type')
        _land = request.POST.get('land')
        _noterfraarkivar = request.POST['noterfraarkivar']
        _noterfratester = request.POST['noterfratester']
        _version = request.POST.get('version')
        _tester = request.POST.get('tester')
        _arkivar = request.POST.get('arkivar')
        _leverandoer = request.POST.get('leverandoer')
        _stoerrelsemb = request.POST.get('stoerrelsemb')
        _afleveringsfrist = request.POST.get('afleveringsfrist')
        _modtaget = request.POST.get('modtaget')
        _adgang = request.POST.get('adgang')
        _svarfrist = request.POST.get('svarfrist')
        _svar = request.POST.get('svar')
        _status = request.POST.get('status')
        _kvitteret = request.POST.get('kvitteret')
        _journaliseret = request.POST.get('journaliseret')
        _kodeord = request.POST.get('kodeord')
        _kopieret = request.POST.get('kopieret')
        _modtagelse = request.POST.get('modtagelse')
        _fileindex = request.POST.get('fileindex')
        _ada = request.POST.get('ada')
        _nedpakket = request.POST.get('nedpakket')
        _maskine_renset = request.POST.get('maskine_renset')
        _fileindex_godkendt = request.POST.get('fileindex_godkendt')
        _dea = request.POST.get('dea')
        _mary_kontrol = request.POST.get('mary_kontrol')
        _meta_opdateret = request.POST.get('meta_opdateret')
        _public_opdateret = request.POST.get('public_opdateret')
        _godkendt_maskine_renset = request.POST.get('godkendt_maskine_renset')

        print('')
        print('----------------------------------------------------------------')
        print('_avid:', _avid)
        print('_jnr:', _jnr)
        print('_public_link:', _public_link)
        print('_titel:', _titel)
        print('_kategori:', _kategori)
        print('_klassifikation:', _klassifikation)
        print('_type:', _type)
        print('_land:', _land)
        print('_noterfraarkivar:', _noterfraarkivar)
        print('_noterfratester:', _noterfratester)
        print('_version:', _version)
        print('_tester:', _tester)
        print('_arkivar:', _arkivar)
        print('_leverandoer:', _leverandoer)
        print('_stoerrelsemb:', _stoerrelsemb)
        print('_afleveringsfrist:', _afleveringsfrist)
        print('_modtaget:', _modtaget)
        print('_adgang:', _adgang)
        print('_svarfrist:', _svarfrist)
        print('_svar:', _svar)
        print('_status:', _status)
        print('_kvitteret:', _kvitteret)
        print('_journaliseret:', _journaliseret)
        print('_kodeord:', _kodeord)
        print('_kopieret:', _kopieret)
        print('_modtagelse:', _modtagelse)
        print('_fileindex:', _fileindex)
        print('_ada:', _ada)
        print('_nedpakket:', _nedpakket)
        print('_maskine_renset:', _maskine_renset)
        print('_fileindex_godkendt:', _fileindex_godkendt)
        print('_dea:', _dea)
        print('_mary_kontrol:', _mary_kontrol)
        print('_meta_opdateret:', _meta_opdateret)
        print('_public_opdateret:', _public_opdateret)
        print('_godkendt_maskine_renset:', _godkendt_maskine_renset)
        print('----------------------------------------------------------------')
        print('')

        return redirect(f'/arkiveringsversioner/arkiveringsversion/{_avid}/{_version}/')

    return render(request, 'arkiveringsversioner/arkiveringsversioner.html', {
        "bruger_rettigheder": rettigheder(request.user),
    })

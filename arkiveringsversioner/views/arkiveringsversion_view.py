from hardware.models.maskine import Maskine
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from datetime import datetime, timedelta
import json

from system.services import rettigheder, tjek_rettigheder
from arkiveringsversioner.models import Arkiveringsversion, Version, Type, Leverandoer, Helligdag, arkiveringsversion, leverandoer
from system.models import Profil, Bruger
from hardware.models import Medie


def tjek(user):
    return tjek_rettigheder(user, {'arkiveringsversioner_arkiveringsversion_se'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def arkiveringsversion_view(request, avid, version=0, nystatus=None):

    if avid == '0' and version == '0' and nystatus == 'opret':

        _avid = request.GET.get('avid_opret')

        if not Arkiveringsversion.objects.filter(avid=_avid).exists():
            _arkiveringsversion_obj = Arkiveringsversion.objects.create(avid=_avid)
            _version_obj = Version.objects.create(nummer=1, avid=_arkiveringsversion_obj, status='Afventer aflevering')
            return redirect(f"/arkiveringsversioner/arkiveringsversion/{_avid}/")
        else:
            return redirect(f"/arkiveringsversioner/arkiveringsversion/{_avid}/")

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

            _version = Version.objects.filter(avid=_arkiveringsversion_obj).order_by('nummer').last().nummer

            version = version if version != 0 else _version

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
                if 'datoformodtagelse' in request.GET:
                    _version_obj.modtaget = datetime.strptime(request.GET.get('datoformodtagelse'), '%d-%m-%Y').date()
                if 'genmodtagetdato' in request.GET:
                    _version_obj.modtaget = datetime.strptime(request.GET.get('genmodtagetdato'), '%d-%m-%Y').date()
                if 'datofortilbagemelding' in request.GET:
                    _version_obj.svar = datetime.strptime(request.GET.get('datofortilbagemelding'), '%d-%m-%Y').date()
                if 'datofortilbagemelding2' in request.GET:
                    _version_obj.svar = datetime.strptime(request.GET.get('datofortilbagemelding2'), '%d-%m-%Y').date()
                if 'datoforafleveringsfrist' in request.GET:
                    _version_obj.genafleveringsfrist = datetime.strptime(request.GET.get('datoforafleveringsfrist'), '%d-%m-%Y').date()
                if 'godkendelsesdato' in request.GET:
                    _version_obj.svar = datetime.strptime(request.GET.get('godkendelsesdato'), '%d-%m-%Y').date()
                    _version_obj.modtaget_kvitteret = False
                    _version_obj.modtaget_journaliseret = False
                    _version_obj.modtaget_kodeord = False
                    _version_obj.modtaget_mangler_kodeord = False
                    _version_obj.modtaget_ikke_krypteret = False
                    _version_obj.modtaget_kopieret = False
                    _version_obj.modtaget_modtagelse_godkendt = False
                    _version_obj.modtaget_modtagelse_afvist = False
                    _version_obj.modtaget_fileindex_kopieret = False
                    _version_obj.modtaget_ada_startet = False
                    _version_obj.modtaget_adatest_godkendt = False
                    _version_obj.modtaget_adatest_afvist = False
                    _version_obj.tilbagemeldt_nedpakket = False
                    _version_obj.tilbagemeldt_maskine_renset = False
                    _version_obj.godkendt_af_tester_fileindex_godkendt = False
                    _version_obj.godkendt_af_tester_afvikler_dea = False
                    _version_obj.godkendt_af_tester_afleveret_til_dea = False
                    _version_obj.godkendt_af_tester_retur_fra_dea = False
                    _version_obj.godkendt_af_tester_mary_kontrol = False
                    _version_obj.godkendt_af_tester_meta_opdateret = False
                    _version_obj.godkendt_af_tester_public_opdateret = False
                    _version_obj.godkendt_af_tester_maskine_renset = False

                if _ny_status == 'Under test':
                    _version_obj.test_begyndt = datetime.today()

                if _ny_status == 'Under test' or _ny_status == 'Tilbagemeldt':
                    _profil_obj = Profil.objects.get(initialer=request.user.username)
                    _bruger_obj = Bruger.objects.get(profil=_profil_obj)
                    _version_obj.tester = _bruger_obj

                if _ny_status == 'Afventer genaflevering':
                    _version_obj.modtaget_kvitteret = False
                    _version_obj.modtaget_journaliseret = False
                    _version_obj.modtaget_kodeord = False
                    _version_obj.modtaget_mangler_kodeord = False
                    _version_obj.modtaget_ikke_krypteret = False
                    _version_obj.modtaget_kopieret = False
                    _version_obj.modtaget_modtagelse_godkendt = False
                    _version_obj.modtaget_modtagelse_afvist = False
                    _version_obj.modtaget_fileindex_kopieret = False
                    _version_obj.modtaget_ada_startet = False
                    _version_obj.modtaget_adatest_godkendt = False
                    _version_obj.modtaget_adatest_afvist = False
                    _version_obj.tilbagemeldt_nedpakket = False
                    _version_obj.tilbagemeldt_maskine_renset = False
                    _version_obj.godkendt_af_tester_fileindex_godkendt = False
                    _version_obj.godkendt_af_tester_afvikler_dea = False
                    _version_obj.godkendt_af_tester_afleveret_til_dea = False
                    _version_obj.godkendt_af_tester_retur_fra_dea = False
                    _version_obj.godkendt_af_tester_mary_kontrol = False
                    _version_obj.godkendt_af_tester_meta_opdateret = False
                    _version_obj.godkendt_af_tester_public_opdateret = False
                    _version_obj.godkendt_af_tester_maskine_renset = False
                    _version_obj.save()
                    Version.objects.create(nummer=_version_obj.nummer+1, avid=_version_obj.avid, status='Afventer genaflevering', arkivar=_version_obj.arkivar, leverandoer=_version_obj.leverandoer, afleveringsfrist=_version_obj.genafleveringsfrist)
                    return redirect(f"/arkiveringsversioner/arkiveringsversion/{avid}/")
                else:
                    _version_obj.status = _ny_status
                    _version_obj.save()
                    return redirect(f"/arkiveringsversioner/arkiveringsversion/{avid}/{version}/")

            _tester_fuldenavn = ''
            if _version_obj.tester:
                if _version_obj.tester.profil.fornavn != '' and _version_obj.tester.profil.fornavn != None:
                    _tester_fuldenavn += _version_obj.tester.profil.fornavn
                if _version_obj.tester.profil.mellemnavn != '' and _version_obj.tester.profil.mellemnavn != None:
                    _tester_fuldenavn += ' '
                    _tester_fuldenavn += _version_obj.tester.profil.mellemnavn
                if _version_obj.tester.profil.efternavn != '' and _version_obj.tester.profil.efternavn != None:
                    _tester_fuldenavn += ' '
                    _tester_fuldenavn += _version_obj.tester.profil.efternavn

            _arkivar_fuldenavn = ''
            if _version_obj.arkivar:
                if _version_obj.arkivar.profil.fornavn != '' and _version_obj.arkivar.profil.fornavn != None:
                    _arkivar_fuldenavn += _version_obj.arkivar.profil.fornavn
                if _version_obj.arkivar.profil.mellemnavn != '' and _version_obj.arkivar.profil.mellemnavn != None:
                    _arkivar_fuldenavn += ' '
                    _arkivar_fuldenavn += _version_obj.arkivar.profil.mellemnavn
                if _version_obj.arkivar.profil.efternavn != '' and _version_obj.arkivar.profil.efternavn != None:
                    _arkivar_fuldenavn += ' '
                    _arkivar_fuldenavn += _version_obj.arkivar.profil.efternavn

            _seneste_version = True if _version_obj.nummer == Version.objects.filter(avid=_version_obj.avid).order_by('nummer').last().nummer else False

            _ibrugtaget_medier = []
            _maskine = None
            _ibrugtaget_medier_objs = Medie.objects.filter(versioner=_version_obj).order_by('navn')
            for _ibrugtaget_medie_obj in _ibrugtaget_medier_objs:
                _ibrugtaget_medier.append({'tag': _ibrugtaget_medie_obj.navn})
                if _ibrugtaget_medie_obj.maskine != None:
                    _maskine = _ibrugtaget_medie_obj.maskine.navn
            _ibrugtaget_medier = json.dumps(_ibrugtaget_medier)

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
                "versioner": Version.objects.filter(avid=_arkiveringsversion_obj),
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
                "maskine": _maskine,
                "modtaget_kvitteret": _version_obj.modtaget_kvitteret,
                "modtaget_journaliseret": _version_obj.modtaget_journaliseret,
                "modtaget_kodeord": _version_obj.modtaget_kodeord,
                "modtaget_mangler_kodeord": _version_obj.modtaget_mangler_kodeord,
                "modtaget_ikke_krypteret": _version_obj.modtaget_ikke_krypteret,
                "modtaget_kopieret": _version_obj.modtaget_kopieret,
                "modtaget_modtagelse_godkendt": _version_obj.modtaget_modtagelse_godkendt,
                "modtaget_modtagelse_afvist": _version_obj.modtaget_modtagelse_afvist,
                "modtaget_fileindex_kopieret": _version_obj.modtaget_fileindex_kopieret,
                "modtaget_ada_startet": _version_obj.modtaget_ada_startet,
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
                "seneste_version": _seneste_version,
                "backtick": '`',
                "ibrugtaget_medier": _ibrugtaget_medier,
            })

        if not Arkiveringsversion.objects.filter(avid=avid).exists():
            messages.error(request, "Den angivet arkiveringsversion findes ikke.")
            return redirect('arkiveringsversioner_view')

    if request.method == 'POST':

        _avid = request.POST.get('avid') if 'avid' in request.POST else None
        _jnr = request.POST.get('jnr') if 'jnr' in request.POST else None
        _public_link = request.POST.get('public_link') if 'public_link' in request.POST else None
        _titel = request.POST.get('titel') if 'titel' in request.POST else None
        _kategori = request.POST.get('kategori') if 'kategori' in request.POST else None
        _klassifikation = request.POST.get('klassifikation') if 'klassifikation' in request.POST else None
        _type = Type.objects.get(navn=request.POST.get('type')) if 'type' in request.POST and request.POST.get('type') != '' else None
        _land = request.POST.get('land') if 'land' in request.POST else None
        _noterfraarkivar = request.POST['noterfraarkivar'] if 'noterfraarkivar' in request.POST else None
        _noterfratester = request.POST['noterfratester'] if 'noterfratester' in request.POST else None
        _version = request.POST.get('version') if 'version' in request.POST else None
        _tester = request.POST.get('tester') if 'tester' in request.POST else None
        _arkivar = request.POST.get('arkivar') if 'arkivar' in request.POST else None
        _leverandoer = Leverandoer.objects.get(navn=request.POST.get('leverandoer')) if 'leverandoer' in request.POST and request.POST.get('leverandoer') != '' else None
        _stoerrelsemb = request.POST.get('stoerrelsemb') if 'stoerrelsemb' in request.POST else None
        _afleveringsfrist = datetime.strptime(request.POST.get('afleveringsfrist'), '%d-%m-%Y').date() if ('afleveringsfrist' in request.POST and request.POST.get('afleveringsfrist') != '') else None
        # _afleveringsfrist = datetime.strptime(request.POST.get('afleveringsfrist'), '%d-%m-%Y').date() if 'afleveringsfrist' in request.POST else None
        # _modtaget = datetime.strptime(request.POST.get('modtaget'), '%d-%m-%Y').date() if 'modtaget' in request.POST else None
        _adgang = datetime.strptime(request.POST.get('adgang'), '%d-%m-%Y').date() if ('adgang' in request.POST and request.POST.get('adgang') != '') else None
        # _svarfrist = datetime.strptime(request.POST.get('svarfrist'), '%d-%m-%Y').date() if 'svarfrist' in request.POST else None
        # _svar = datetime.strptime(request.POST.get('svar'), '%d-%m-%Y').date() if 'svar' in request.POST else None
        # _status = request.POST.get('status') if 'status' in request.POST else None
        _kvitteret = request.POST.get('kvitteret') if 'kvitteret' in request.POST else None
        _journaliseret = request.POST.get('journaliseret') if 'journaliseret' in request.POST else None
        _kodeord = request.POST.get('kodeord') if 'kodeord' in request.POST else None
        _kopieret = request.POST.get('kopieret') if 'kopieret' in request.POST else None
        _modtagelse = request.POST.get('modtagelse') if 'modtagelse' in request.POST else None
        _fileindex = request.POST.get('fileindex') if 'fileindex' in request.POST else None
        _ada_startet = request.POST.get('ada_startet') if 'ada_startet' in request.POST else None
        _ada = request.POST.get('ada') if 'ada' in request.POST else None
        _nedpakket = request.POST.get('nedpakket') if 'nedpakket' in request.POST else None
        _maskine_renset = request.POST.get('maskine_renset') if 'maskine_renset' in request.POST else None
        _fileindex_godkendt = request.POST.get('fileindex_godkendt') if 'fileindex_godkendt' in request.POST else None
        _dea = request.POST.get('dea') if 'dea' in request.POST else None
        _mary_kontrol = request.POST.get('mary_kontrol') if 'mary_kontrol' in request.POST else None
        _meta_opdateret = request.POST.get('meta_opdateret') if 'meta_opdateret' in request.POST else None
        _public_opdateret = request.POST.get('public_opdateret') if 'public_opdateret' in request.POST else None
        _godkendt_maskine_renset = request.POST.get('godkendt_maskine_renset') if 'godkendt_maskine_renset' in request.POST else None
        _medier = request.POST.get('av_medier') if 'av_medier' in request.POST else None
        _old_medier = request.POST.get('old_medier') if 'old_medier' in request.POST else None

        _arkiveringsversion_obj = None
        _version_obj = None

        if Arkiveringsversion.objects.filter(avid=_avid).exists():
            _arkiveringsversion_obj = Arkiveringsversion.objects.get(avid=_avid)

            if Version.objects.filter(nummer=_version, avid=_arkiveringsversion_obj).exists():
                _version_obj = Version.objects.get(nummer=_version, avid=_arkiveringsversion_obj)

            if not Version.objects.filter(nummer=_version, avid=_arkiveringsversion_obj).exists():
                messages.error(request, f"Den angivet version af arkiveringsversionen 'AVID.SA.{avid}' findes ikke.")
                return redirect('arkiveringsversioner_view')

            _arkiveringsversion_obj.jnr = _jnr if _jnr else _arkiveringsversion_obj.jnr
            _arkiveringsversion_obj.public = _public_link if _public_link else _arkiveringsversion_obj.public
            _arkiveringsversion_obj.titel = _titel if _titel else _arkiveringsversion_obj.titel
            _arkiveringsversion_obj.kategori = _kategori if _kategori != None else _arkiveringsversion_obj.kategori
            _arkiveringsversion_obj.klassifikation = _klassifikation if _klassifikation != None else _arkiveringsversion_obj.klassifikation
            _arkiveringsversion_obj.type = _type
            _arkiveringsversion_obj.land = _land if _land else _arkiveringsversion_obj.land
            _arkiveringsversion_obj.arkivar_noter = _noterfraarkivar if _noterfraarkivar != None else _arkiveringsversion_obj.arkivar_noter
            _arkiveringsversion_obj.tester_noter = _noterfratester if _noterfratester != None else _arkiveringsversion_obj.tester_noter
            _arkiveringsversion_obj.save()

            if _tester:
                _profil_obj = Profil.objects.get(initialer=_tester)
                _bruger_obj = Bruger.objects.get(profil=_profil_obj)
                _version_obj.tester = _bruger_obj
            elif _tester == '':
                _version_obj.tester = None

            if _arkivar:
                _profil_obj = Profil.objects.get(initialer=_arkivar)
                _bruger_obj = Bruger.objects.get(profil=_profil_obj)
                _version_obj.arkivar = _bruger_obj
            elif _arkivar == '':
                _version_obj.arkivar = None

            if _leverandoer:
                _version_obj.leverandoer = _leverandoer
            elif _leverandoer == None:
                _version_obj.leverandoer = None

            _version_obj.adgang = _adgang
            _version_obj.afleveringsfrist = _afleveringsfrist

            if _version_obj.adgang:
                _version_obj.svarfrist = add_days(_version_obj.adgang, 90)

            _version_obj.stoerrelsemb = _stoerrelsemb if _stoerrelsemb else _version_obj.stoerrelsemb
            _version_obj.modtaget_kvitteret = True if _kvitteret == 'kvitteret' else False
            _version_obj.modtaget_journaliseret = True if _journaliseret == 'journaliseret' else False

            if _kodeord == None:
                _version_obj.modtaget_kodeord = False
                _version_obj.modtaget_mangler_kodeord = False
                _version_obj.modtaget_ikke_krypteret = False
            elif _kodeord == 'modtaget':
                _version_obj.modtaget_kodeord = True
                _version_obj.modtaget_mangler_kodeord = False
                _version_obj.modtaget_ikke_krypteret = False
            elif _kodeord == 'mangler':
                _version_obj.modtaget_kodeord = False
                _version_obj.modtaget_mangler_kodeord = True
                _version_obj.modtaget_ikke_krypteret = False
            elif _kodeord == 'ikke_krypteret':
                _version_obj.modtaget_kodeord = False
                _version_obj.modtaget_mangler_kodeord = False
                _version_obj.modtaget_ikke_krypteret = True

            _version_obj.modtaget_kopieret = True if _kopieret == 'kopieret' else False

            if _modtagelse == None:
                _version_obj.modtaget_modtagelse_godkendt = False
                _version_obj.modtaget_modtagelse_afvist = False
            elif _modtagelse == 'godkendt':
                _version_obj.modtaget_modtagelse_godkendt = True
                _version_obj.modtaget_modtagelse_afvist = False
            elif _modtagelse == 'afvist':
                _version_obj.modtaget_modtagelse_godkendt = False
                _version_obj.modtaget_modtagelse_afvist = True

            _version_obj.modtaget_fileindex_kopieret = True if _fileindex == 'kopieret' else False

            _version_obj.modtaget_ada_startet = True if _ada_startet == 'startet' else False

            if _ada == None:
                _version_obj.modtaget_adatest_godkendt = False
                _version_obj.modtaget_adatest_afvist = False
            elif _ada == 'godkendt':
                _version_obj.modtaget_adatest_godkendt = True
                _version_obj.modtaget_adatest_afvist = False
            elif _ada == 'afvist':
                _version_obj.modtaget_adatest_godkendt = False
                _version_obj.modtaget_adatest_afvist = True

            _version_obj.tilbagemeldt_nedpakket = True if _nedpakket == 'nedpakket' else False
            _version_obj.tilbagemeldt_maskine_renset = True if _maskine_renset == 'maskine_renset' else False

            _version_obj.godkendt_af_tester_fileindex_godkendt = True if _fileindex_godkendt else False

            if _dea == None:
                _version_obj.godkendt_af_tester_afvikler_dea = False
                _version_obj.godkendt_af_tester_afleveret_til_dea = False
                _version_obj.godkendt_af_tester_retur_fra_dea = False
            elif _dea == 'afvikler':
                _version_obj.godkendt_af_tester_afvikler_dea = True
                _version_obj.godkendt_af_tester_afleveret_til_dea = False
                _version_obj.godkendt_af_tester_retur_fra_dea = False
            elif _dea == 'afleveret':
                _version_obj.godkendt_af_tester_afvikler_dea = False
                _version_obj.godkendt_af_tester_afleveret_til_dea = True
                _version_obj.godkendt_af_tester_retur_fra_dea = False
            elif _dea == 'retur':
                _version_obj.godkendt_af_tester_afvikler_dea = False
                _version_obj.godkendt_af_tester_afleveret_til_dea = False
                _version_obj.godkendt_af_tester_retur_fra_dea = True

            _version_obj.godkendt_af_tester_mary_kontrol = True if _mary_kontrol == 'mary_kontrol' else False
            _version_obj.godkendt_af_tester_meta_opdateret = True if _meta_opdateret == 'meta_opdateret' else False
            _version_obj.godkendt_af_tester_public_opdateret = True if _public_opdateret == 'public_opdateret' else False
            _version_obj.godkendt_af_tester_maskine_renset = True if _godkendt_maskine_renset == 'godkendt_maskine_renset' else False

            old_medier = []
            if _old_medier:
                for m in json.loads(_old_medier):
                    old_medier.append(m['tag'].upper())
                for old_medie in old_medier:
                    old_m = Medie.objects.filter(navn=old_medie).first()
                    if old_m:
                        old_m.versioner.remove(_version_obj)

            medier = []
            if _medier:
                for m in json.loads(_medier):
                    medier.append(m['tag'].upper())
                for medie in medier:
                    m = Medie.objects.filter(navn=medie).first()
                    if m:
                        m.versioner.add(_version_obj)
                    else:
                        messages.error(request, f"Mediet '{medie}' findes ikke.")

            print(len(medier))
            if len(medier) > 0:
                _version_obj.modtaget_kopieret = True
            else:
                _version_obj.modtaget_kopieret = False

            _version_obj.save()

            return redirect(f"/arkiveringsversioner/arkiveringsversion/{avid}/{version}/")

        if not Arkiveringsversion.objects.filter(avid=_avid).exists():
            messages.error(request, "Den angivet arkiveringsversion findes ikke.")
            return redirect('arkiveringsversioner_view')

    return render(request, 'arkiveringsversioner/arkiveringsversioner.html', {
        "bruger_rettigheder": rettigheder(request.user),
    })


def add_days(start_date, added_days):
    holidays = []

    holiday_objs = Helligdag.objects.all()
    for holiday_obj in holiday_objs:
        holidays.append(holiday_obj.dag)

    days_elapsed = 0
    while days_elapsed < added_days:
        test_date = start_date + timedelta(days=1)
        start_date = test_date
        if test_date in holidays:
            continue
        else:
            days_elapsed += 1

    return start_date

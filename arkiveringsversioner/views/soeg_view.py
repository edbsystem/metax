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
def soeg_view(request, nulstil=0):

    _avid = request.GET.get('avid_soeg') if 'avid_soeg' in request.GET and request.GET.get('avid_soeg') != '' else None
    _jnr = request.GET.get('jnr_soeg') if 'jnr_soeg' in request.GET and request.GET.get('jnr_soeg') != '' else None
    _titel = request.GET.get('titel_soeg') if 'titel_soeg' in request.GET and request.GET.get('titel_soeg') != '' else None
    _land = request.GET.getlist('land_soeg') if 'land_soeg' in request.GET else None
    _status = request.GET.getlist('status_soeg') if 'status_soeg' in request.GET else None
    _kategori = request.GET.getlist('kategori_soeg') if 'kategori_soeg' in request.GET else None
    _klassifikation = request.GET.getlist('klassifikation_soeg') if 'klassifikation_soeg' in request.GET else None
    _type = request.GET.getlist('type_soeg') if 'type_soeg' in request.GET else None
    _arkivar = request.GET.getlist('arkivar_soeg') if 'arkivar_soeg' in request.GET else None
    _leverandoer = request.GET.getlist('leverandoer_soeg') if 'leverandoer_soeg' in request.GET else None
    _tester = request.GET.getlist('tester_soeg') if 'tester_soeg' in request.GET else None
    _afleveringsfrist_fra = datetime.strptime(request.GET.get('afleveringsfrist_fra_soeg'), '%d-%m-%Y').date() if 'afleveringsfrist_fra_soeg' in request.GET and request.GET.get('afleveringsfrist_fra_soeg') != '' else None
    _afleveringsfrist_til = datetime.strptime(request.GET.get('afleveringsfrist_til_soeg'), '%d-%m-%Y').date() if 'afleveringsfrist_til_soeg' in request.GET and request.GET.get('afleveringsfrist_til_soeg') != '' else None
    _modtaget_fra = datetime.strptime(request.GET.get('modtaget_fra_soeg'), '%d-%m-%Y').date() if 'modtaget_fra_soeg' in request.GET and request.GET.get('modtaget_fra_soeg') != '' else None
    _modtaget_til = datetime.strptime(request.GET.get('modtaget_til_soeg'), '%d-%m-%Y').date() if 'modtaget_til_soeg' in request.GET and request.GET.get('modtaget_til_soeg') != '' else None
    _adgang_fra = datetime.strptime(request.GET.get('adgang_fra_soeg'), '%d-%m-%Y').date() if 'adgang_fra_soeg' in request.GET and request.GET.get('adgang_fra_soeg') != '' else None
    _adgang_til = datetime.strptime(request.GET.get('adgang_til_soeg'), '%d-%m-%Y').date() if 'adgang_til_soeg' in request.GET and request.GET.get('adgang_til_soeg') != '' else None
    _svarfrist_fra = datetime.strptime(request.GET.get('svarfrist_fra_soeg'), '%d-%m-%Y').date() if 'svarfrist_fra_soeg' in request.GET and request.GET.get('svarfrist_fra_soeg') != '' else None
    _svarfrist_til = datetime.strptime(request.GET.get('svarfrist_til_soeg'), '%d-%m-%Y').date() if 'svarfrist_til_soeg' in request.GET and request.GET.get('svarfrist_til_soeg') != '' else None
    _genafleveringsfrist_fra = datetime.strptime(request.GET.get('genafleveringsfrist_fra_soeg'), '%d-%m-%Y').date() if 'genafleveringsfrist_fra_soeg' in request.GET and request.GET.get('genafleveringsfrist_fra_soeg') != '' else None
    _genafleveringsfrist_til = datetime.strptime(request.GET.get('genafleveringsfrist_til_soeg'), '%d-%m-%Y').date() if 'genafleveringsfrist_til_soeg' in request.GET and request.GET.get('genafleveringsfrist_til_soeg') != '' else None
    _svar_fra = datetime.strptime(request.GET.get('svar_fra_soeg'), '%d-%m-%Y').date() if 'svar_fra_soeg' in request.GET and request.GET.get('svar_fra_soeg') != '' else None
    _svar_til = datetime.strptime(request.GET.get('svar_til_soeg'), '%d-%m-%Y').date() if 'svar_til_soeg' in request.GET and request.GET.get('svar_til_soeg') != '' else None
    _enkelte_versioner = True if request.GET.get('enkelte_versioner') != None else False
    _vis_avid = True if request.GET.get('vis_avid') != None else False
    _vis_version = True if request.GET.get('vis_version') != None else False
    _vis_jnr = True if request.GET.get('vis_jnr') != None else False
    _vis_titel = True if request.GET.get('vis_titel') != None else False
    _vis_land = True if request.GET.get('vis_land') != None else False
    _vis_status = True if request.GET.get('vis_status') != None else False
    _vis_kategori = True if request.GET.get('vis_kategori') != None else False
    _vis_klassifikation = True if request.GET.get('vis_klassifikation') != None else False
    _vis_type = True if request.GET.get('vis_type') != None else False
    _vis_arkivar = True if request.GET.get('vis_arkivar') != None else False
    _vis_leverandoer = True if request.GET.get('vis_leverandoer') != None else False
    _vis_tester = True if request.GET.get('vis_tester') != None else False
    _vis_afleveringsfrist = True if request.GET.get('vis_afleveringsfrist') != None else False
    _vis_modtaget = True if request.GET.get('vis_modtaget') != None else False
    _vis_adgang = True if request.GET.get('vis_adgang') != None else False
    _vis_svarfrist = True if request.GET.get('vis_svarfrist') != None else False
    _vis_genafleveringsfrist = True if request.GET.get('vis_genafleveringsfrist') != None else False
    _vis_svar = True if request.GET.get('vis_svar') != None else False

    _resultat = list()

    if nulstil:
        _vis_avid = True
        _vis_version = True
        _vis_jnr = True
        _vis_titel = True
        _vis_status = True
        _vis_kategori = True

    if not nulstil:
        _avs_objs = Arkiveringsversion.objects.all()
        if _avid:
            _avs_objs = _avs_objs.filter(avid__icontains=_avid)
        if _jnr:
            _avs_objs = _avs_objs.filter(jnr__icontains=_jnr)
        if _titel:
            _avs_objs = _avs_objs.filter(titel__icontains=_titel)
        if _land:
            _avs_objs = _avs_objs.filter(qtq([Q(land=value) for value in _land]))
        if _kategori:
            _avs_objs = _avs_objs.filter(qtq([Q(kategori=value) for value in _kategori]))
        if _klassifikation:
            _avs_objs = _avs_objs.filter(qtq([Q(klassifikation=value) for value in _klassifikation]))
        if _type:
            _avs_objs = _avs_objs.filter(qtq([Q(type=value) for value in [Type.objects.get(navn=value) for value in _type]]))

        _version_objs = Version.objects.filter(avid__in=(av for av in _avs_objs))
        if _status:
            _version_objs = _version_objs.filter(qtq([Q(status=value) for value in _status]))
        if _arkivar:
            _version_objs = _version_objs.filter(qtq([Q(arkivar=Bruger.objects.get(profil=value)) for value in [Profil.objects.get(initialer=value) for value in _arkivar]]))
        if _leverandoer:
            _version_objs = _version_objs.filter(qtq([Q(leverandoer=value) for value in [Leverandoer.objects.get(navn=value) for value in _leverandoer]]))
        if _tester:
            _version_objs = _version_objs.filter(qtq([Q(tester=Bruger.objects.get(profil=value)) for value in [Profil.objects.get(initialer=value) for value in _tester]]))
        if _afleveringsfrist_fra:
            _version_objs = _version_objs.filter(Q(afleveringsfrist__gte=_afleveringsfrist_fra) | ~Q(afleveringsfrist=None))
        if _afleveringsfrist_til:
            _version_objs = _version_objs.filter(Q(afleveringsfrist__lte=_afleveringsfrist_til) | ~Q(afleveringsfrist=None))
        if _modtaget_fra:
            _version_objs = _version_objs.filter(Q(modtaget__gte=_modtaget_fra) | ~Q(modtaget=None))
        if _modtaget_til:
            _version_objs = _version_objs.filter(Q(modtaget__lte=_modtaget_til) | ~Q(modtaget=None))
        if _adgang_fra:
            _version_objs = _version_objs.filter(Q(adgang__gte=_adgang_fra) | ~Q(adgang=None))
        if _adgang_til:
            _version_objs = _version_objs.filter(Q(adgang__lte=_adgang_til) | ~Q(adgang=None))
        if _svarfrist_fra:
            _version_objs = _version_objs.filter(Q(svarfrist__gte=_svarfrist_fra) | ~Q(svarfrist=None))
        if _svarfrist_til:
            _version_objs = _version_objs.filter(Q(svarfrist__lte=_svarfrist_til) | ~Q(svarfrist=None))
        if _genafleveringsfrist_fra:
            _version_objs = _version_objs.filter(Q(genafleveringsfrist__gte=_genafleveringsfrist_fra) | ~Q(genafleveringsfrist=None))
        if _genafleveringsfrist_til:
            _version_objs = _version_objs.filter(Q(genafleveringsfrist__lte=_genafleveringsfrist_til) | ~Q(genafleveringsfrist=None))
        if _svar_fra:
            _version_objs = _version_objs.filter(Q(svar__gte=_svar_fra) | ~Q(svar=None))
        if _svar_til:
            _version_objs = _version_objs.filter(Q(svar__lte=_svar_til) | ~Q(svar=None))

        if _enkelte_versioner:
            for version in _version_objs:
                _resultat.append({
                    "avid": version.avid.avid,
                    "version": version.nummer,
                    "jnr": version.avid.jnr,
                    "titel": version.avid.titel,
                    "land": version.avid.land,
                    "status": version.status,
                    "kategori": version.avid.kategori,
                    "klassifikation": version.avid.klassifikation,
                    "type": version.avid.type if version.avid.type else '',
                    "arkivar": version.arkivar if version.arkivar else '',
                    "leverandoer": version.leverandoer,
                    "tester": version.tester if version.tester else '',
                    "afleveringsfrist": '{:%d-%m-%Y}'.format(version.afleveringsfrist) if version.afleveringsfrist != None else '',
                    "modtaget": '{:%d-%m-%Y}'.format(version.modtaget) if version.modtaget != None else '',
                    "adgang": '{:%d-%m-%Y}'.format(version.adgang) if version.adgang != None else '',
                    "svarfrist": '{:%d-%m-%Y}'.format(version.svarfrist) if version.svarfrist != None else '',
                    "genafleveringsfrist": '{:%d-%m-%Y}'.format(version.genafleveringsfrist) if version.genafleveringsfrist != None else '',
                    "svar": '{:%d-%m-%Y}'.format(version.svar) if version.svar != None else '',
                })

        if not _enkelte_versioner:
            avs = set()
            for version in _version_objs:
                avs.add(version.avid.avid)
            for avid in avs:
                av = Arkiveringsversion.objects.get(avid=avid)
                version_last = Version.objects.filter(avid=av).order_by('nummer').last()
                _resultat.append({
                    "avid": av.avid,
                    "jnr": av.jnr,
                    "titel": av.titel,
                    "land": av.land,
                    "status": version_last.status,
                    "kategori": av.kategori,
                    "klassifikation": av.klassifikation,
                    "type": av.type if av.type else '',
                    "arkivar": version_last.arkivar if version_last.arkivar else '',
                    "leverandoer": version_last.leverandoer if version_last.leverandoer else '',
                    "tester": version_last.tester if version_last.tester else '',
                    "afleveringsfrist": '{:%d-%m-%Y}'.format(version_last.afleveringsfrist) if version_last.afleveringsfrist != None else '',
                    "modtaget": '{:%d-%m-%Y}'.format(version_last.modtaget) if version_last.modtaget != None else '',
                    "adgang": '{:%d-%m-%Y}'.format(version_last.adgang) if version_last.adgang != None else '',
                    "svarfrist": '{:%d-%m-%Y}'.format(version_last.svarfrist) if version_last.svarfrist != None else '',
                    "genafleveringsfrist": '{:%d-%m-%Y}'.format(version_last.genafleveringsfrist) if version_last.genafleveringsfrist != None else '',
                    "svar": '{:%d-%m-%Y}'.format(version_last.svar) if version_last.svar != None else '',
                })

    return render(request, 'arkiveringsversioner/soeg.html', {
        "bruger_rettigheder": rettigheder(request.user),
        "avid": _avid,
        "jnr": _jnr,
        "titel": _titel,
        "land": _land,
        "status": _status,
        "kategori": _kategori,
        "klassifikation": _klassifikation,
        "type": _type,
        "arkivar": _arkivar,
        "leverandoer": _leverandoer,
        "tester": _tester,
        "afleveringsfrist_fra": _afleveringsfrist_fra,
        "afleveringsfrist_til": _afleveringsfrist_til,
        "modtaget_fra": _modtaget_fra,
        "modtaget_til": _modtaget_til,
        "adgang_fra": _adgang_fra,
        "adgang_til": _adgang_til,
        "svarfrist_fra": _svarfrist_fra,
        "svarfrist_til": _svarfrist_til,
        "genafleveringsfrist_fra": _genafleveringsfrist_fra,
        "genafleveringsfrist_til": _genafleveringsfrist_til,
        "svar_fra": _svar_fra,
        "svar_til": _svar_til,
        "enkelte_versioner": _enkelte_versioner,
        "nulstil": nulstil,
        "vis_avid": _vis_avid,
        "vis_version": _vis_version,
        "vis_jnr": _vis_jnr,
        "vis_titel": _vis_titel,
        "vis_land": _vis_land,
        "vis_status": _vis_status,
        "vis_kategori": _vis_kategori,
        "vis_klassifikation": _vis_klassifikation,
        "vis_type": _vis_type,
        "vis_arkivar": _vis_arkivar,
        "vis_leverandoer": _vis_leverandoer,
        "vis_tester": _vis_tester,
        "vis_afleveringsfrist": _vis_afleveringsfrist,
        "vis_modtaget": _vis_modtaget,
        "vis_adgang": _vis_adgang,
        "vis_svarfrist": _vis_svarfrist,
        "vis_genafleveringsfrist": _vis_genafleveringsfrist,
        "vis_svar": _vis_svar,
        # "arkiveringsversioner": _avs_objs,
        # "versioner": _version_objs,
        "resultat": _resultat,
    })


def qtq(queries):
    query = queries.pop()
    for item in queries:
        query |= item
    return query

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

from system.services import rettigheder, tjek_rettigheder
from arkiveringsversioner.models import Arkiveringsversion, Type, Version
from system.models import Bruger, Profil


def tjek(user):
    return tjek_rettigheder(user, {'arkiveringsversioner_se'})


@user_passes_test(tjek, login_url='/', redirect_field_name=None)
def soeg_view(request):

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
    _afleveringsfrist_fra = request.GET.get('afleveringsfrist_fra_soeg') if 'afleveringsfrist_fra_soeg' in request.GET and request.GET.get('afleveringsfrist_fra_soeg') != '' else None
    _afleveringsfrist_til = request.GET.get('afleveringsfrist_til_soeg') if 'afleveringsfrist_til_soeg' in request.GET and request.GET.get('afleveringsfrist_til_soeg') != '' else None
    _modtaget_fra = request.GET.get('modtaget_fra_soeg') if 'modtaget_fra_soeg' in request.GET and request.GET.get('modtaget_fra_soeg') != '' else None
    _modtaget_til = request.GET.get('modtaget_til_soeg') if 'modtaget_til_soeg' in request.GET and request.GET.get('modtaget_til_soeg') != '' else None
    _adgang_fra = request.GET.get('adgang_fra_soeg') if 'adgang_fra_soeg' in request.GET and request.GET.get('adgang_fra_soeg') != '' else None
    _adgang_til = request.GET.get('adgang_til_soeg') if 'adgang_til_soeg' in request.GET and request.GET.get('adgang_til_soeg') != '' else None
    _svarfrist_fra = request.GET.get('svarfrist_fra_soeg') if 'svarfrist_fra_soeg' in request.GET and request.GET.get('svarfrist_fra_soeg') != '' else None
    _svarfrist_til = request.GET.get('svarfrist_til_soeg') if 'svarfrist_til_soeg' in request.GET and request.GET.get('svarfrist_til_soeg') != '' else None
    _genafleveringsfrist_fra = request.GET.get('genafleveringsfrist_fra_soeg') if 'genafleveringsfrist_fra_soeg' in request.GET and request.GET.get('genafleveringsfrist_fra_soeg') != '' else None
    _genafleveringsfrist_til = request.GET.get('genafleveringsfrist_til_soeg') if 'genafleveringsfrist_til_soeg' in request.GET and request.GET.get('genafleveringsfrist_til_soeg') != '' else None
    _svar_fra = request.GET.get('svar_fra_soeg') if 'svar_fra_soeg' in request.GET and request.GET.get('svar_fra_soeg') != '' else None
    _svar_til = request.GET.get('svar_til_soeg') if 'svar_til_soeg' in request.GET and request.GET.get('svar_til_soeg') != '' else None

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
    if _tester:
        _version_objs = _version_objs.filter(qtq([Q(tester=Bruger.objects.get(profil=value)) for value in [Profil.objects.get(initialer=value) for value in _tester]]))

    return render(request, 'arkiveringsversioner/soeg.html', {
        "bruger_rettigheder": rettigheder(request.user),
        "arkiveringsversioner": _avs_objs,
        "versioner": _version_objs
    })


def qtq(queries):
    query = queries.pop()
    for item in queries:
        query |= item
    return query

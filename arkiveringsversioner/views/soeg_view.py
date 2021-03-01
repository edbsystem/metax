from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from itertools import chain

from system.services import rettigheder, tjek_rettigheder
from arkiveringsversioner.models import Arkiveringsversion, Type, Version


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

    # print('avid_soeg:', _avid)
    # print('jnr_soeg:', _jnr)
    # print('titel_soeg:', _titel)
    # print('land_soeg:', _land)
    # print('status_soeg:', _status)
    # print('kategori_soeg:', _kategori)
    # print('klassifikation_soeg:', _klassifikation)
    # print('type_soeg:', _type)
    # print('arkivar_soeg:', _arkivar)
    # print('leverandoer_soeg:', _leverandoer)
    # print('tester_soeg:', _tester)
    # print('afleveringsfrist_fra_soeg:', _afleveringsfrist_fra)
    # print('afleveringsfrist_til_soeg:', _afleveringsfrist_til)
    # print('modtaget_fra_soeg:', _modtaget_fra)
    # print('modtaget_til_soeg:', _modtaget_til)
    # print('adgang_fra_soeg:', _adgang_fra)
    # print('adgang_til_soeg:', _adgang_til)
    # print('svarfrist_fra_soeg:', _svarfrist_fra)
    # print('svarfrist_til_soeg:', _svarfrist_til)
    # print('genafleveringsfrist_fra_soeg:', _genafleveringsfrist_fra)
    # print('genafleveringsfrist_til_soeg:', _genafleveringsfrist_til)
    # print('svar_fra_soeg:', _svar_fra)
    # print('svar_til_soeg:', _svar_til)

    avs_objs = Arkiveringsversion.objects.all()

    if _avid:
        avs_objs = avs_objs.filter(avid__icontains=_avid)

    if _jnr:
        avs_objs = avs_objs.filter(jnr__icontains=_jnr)

    if _titel:
        avs_objs = avs_objs.filter(titel__icontains=_titel)

    if _land:
        queries = [Q(land=value) for value in _land]
        query = queries.pop()
        for item in queries:
            query |= item
        avs_objs = avs_objs.filter(query)

    if _kategori:
        queries = [Q(kategori=value) for value in _kategori]
        query = queries.pop()
        for item in queries:
            query |= item
        avs_objs = avs_objs.filter(query)

    if _klassifikation:
        queries = [Q(klassifikation=value) for value in _klassifikation]
        query = queries.pop()
        for item in queries:
            query |= item
        avs_objs = avs_objs.filter(query)

    if _type:
        _type_objs = [Type.objects.get(navn=value) for value in _type]
        queries = [Q(type=value) for value in _type_objs]
        query = queries.pop()
        for item in queries:
            query |= item
        avs_objs = avs_objs.filter(query)

    _version_objs = Version.objects.filter(avid__in=(av for av in avs_objs))

    return render(request, 'arkiveringsversioner/soeg.html', {
        "bruger_rettigheder": rettigheder(request.user),
        "arkiveringsversioner": avs_objs,
    })

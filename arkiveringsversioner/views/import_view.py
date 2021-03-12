from django.shortcuts import render, redirect
import sqlite3
import re
from datetime import datetime
from django.contrib.auth.models import User

from arkiveringsversioner.models import Arkiveringsversion, Version, Leverandoer, Type
from system.models import Profil, Bruger


def import_view(request):

    # slet alle eksisterende arkiveringsversioner i metax

    Arkiveringsversion.objects.all().delete()

    # import alle gamle arkiveringsversioner fra meta

    av_conn = sqlite3.connect(f'''C:\\Users\\Thomas\\Repos\\metax\\old_db.sqlite3''')
    av_cursor = av_conn.cursor()
    av_cursor.execute('''select * from avs_av''')
    av_rows = av_cursor.fetchall()

    for av_row in av_rows:

        # opret arkiveringsversion

        avid = av_row[1] if av_row[1] else None
        jnr = av_row[3] if av_row[3] else None
        titel = av_row[4] if av_row[4] else None

        if av_row[5] == 'Stat':
            kategori = 'Statslig'
        elif av_row[5] == 'Kommune':
            kategori = 'Kommunal'
        elif av_row[5] == 'Privat':
            kategori = 'Privat'
        elif av_row[5] == 'Klassificeret':
            kategori = 'Statslig'
        elif av_row[5] == 'Forskningsdata':
            kategori = 'Forskning'
        else:
            kategori = None

        if av_row[6] == 'Ingen':
            klassifikation = 'Ingen'
        elif av_row[6] == 'Til tjenestebrug':
            klassifikation = 'Til tjenestebrug'
        elif av_row[6] == 'Andet':
            klassifikation = 'Andet'
        else:
            klassifikation = None

        land = av_row[7] if av_row[7] else None

        type = Type.objects.get(navn='DST') if av_row[16] == 258 else None

        public = re.search("(https:).*", av_row[23]).group() if av_row[23] else None

        if not Arkiveringsversion.objects.filter(avid=avid).exists():
            Arkiveringsversion.objects.create(avid=avid, jnr=jnr, public=public, titel=titel, kategori=kategori, klassifikation=klassifikation, land=land, type=type)

        # opret versioner

        version = av_row[2] if av_row[2] else None

        if av_row[13] == 'Afleveret til DEA':
            status = 'Modtaget'
        elif av_row[13] == 'Afventer genaflevering':
            status = 'Afventer genaflevering'
        elif av_row[13] == 'Afvikler ADA':
            status = 'Modtaget'
        elif av_row[13] == 'Forhåndsgodkendt af tester':
            status = 'Godkendt af tester'
        elif av_row[13] == 'Godkendt':
            status = 'Godkendt'
        elif av_row[13] == 'Journaliseret':
            status = 'Modtaget'
        elif av_row[13] == 'Klar til test':
            status = 'Klar til test'
        elif av_row[13] == 'Kopieret':
            status = 'Modtaget'
        elif av_row[13] == 'Kvitteret':
            status = 'Modtaget'
        elif av_row[13] == 'Mangler kodeord':
            status = 'Modtaget'
        elif av_row[13] == 'Oprettet':
            status = 'Modtaget'
        elif av_row[13] == 'Tilbagemeldt':
            status = 'Tilbagemeldt'
        elif av_row[13] == 'Under test':
            status = 'Under test'
        else:
            status = None

        stoerrelse = 0
        modtaget = datetime.strptime(av_row[9], '%Y-%m-%d').date() if av_row[9] else None
        adgang = datetime.strptime(av_row[10], '%Y-%m-%d').date() if av_row[10] else None
        svarfrist = datetime.strptime(av_row[11], '%Y-%m-%d').date() if av_row[11] else None
        svar = datetime.strptime(av_row[12], '%Y-%m-%d').date() if av_row[12] else None
        leverandoer = Leverandoer.objects.get(pk=av_row[16]) if av_row[16] else None

        # TODO: if av_row[16] = hvad der svarer til DST så Selvlavet, og opret type DST og så denne

        testere = {4: 'THH', 5: 'IHA', 6: 'SLL', 7: 'NRS', 8: 'BGJ', 9: 'PMT', 10: 'JDS', 11: 'ABN', 12: 'REM', 13: 'AKE', 14: 'IGC', 15: 'FHK', 16: 'ASS', 17: 'TBO', 18: 'PBP', 19: 'USN', 20: 'KVG', 21: 'STL', 23: 'LUK', 24: 'IHL', 25: 'CBM'}

        tester = None
        if av_row[18]:
            initialer = testere[av_row[18]] if av_row[18] != 1 else None

            if initialer:
                user_obj = User.objects.get(username=initialer)
                profil_obj = Profil.objects.get(initialer=user_obj.username)
                tester = Bruger.objects.get(profil=profil_obj)

        if version and not Version.objects.filter(avid=avid, nummer=version).exists():
            _avid = Arkiveringsversion.objects.get(avid=avid)
            Version.objects.create(avid=_avid, nummer=version, status=status, stoerrelsemb=stoerrelse, leverandoer=leverandoer, modtaget=modtaget, adgang=adgang, svarfrist=svarfrist, svar=svar, tester=tester)

    return redirect('arkiveringsversioner_view')

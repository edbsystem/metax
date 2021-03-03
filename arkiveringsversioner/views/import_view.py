from django.shortcuts import render
import sqlite3
import re

from arkiveringsversioner.models import Arkiveringsversion, Version, Leverandoer


def import_view(request):

    av_conn = sqlite3.connect(f'''C:\\Users\\Thomas\\Repos\\metax\\old_db.sqlite3''')
    av_cursor = av_conn.cursor()
    av_cursor.execute('''select * from avs_av''')

    av_rows = av_cursor.fetchall()

    avids = set()

    Arkiveringsversion.objects.all().delete()

    for av_row in av_rows:
        avid = av_row[1] if av_row[1] else None
        version = av_row[2] if av_row[2] else None
        jnr = av_row[3] if av_row[3] else None
        titel = av_row[4] if av_row[4] else None

        if av_row[5] == 'Stat':
            kategori = 'Statslig'
        elif av_row[5] == 'Kommune':
            kategori = 'Kommunal'
        elif av_row[5] == 'Privat':
            kategori = 'Privat'
        elif av_row[5] == 'Klassificeret':
            kategori = 'Stat'
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
        stoerrelse = 0
        modtaget = av_row[9] if av_row[9] else None
        adgang = av_row[10] if av_row[10] else None
        svarfrist = av_row[11] if av_row[11] else None
        svar = av_row[12] if av_row[12] else None

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

        # if av_row[16] = hvad der svarer til DST så Selvlavet
        leverandoer = Leverandoer.objects.get(pk=av_row[16]) if av_row[16] else None
        public = re.search("(https:).*", av_row[23]).group() if av_row[23] else None

        if avid not in avids:
            avids.add(avid)
            Arkiveringsversion.objects.create(avid=avid, jnr=jnr, public=public, titel=titel, kategori=kategori, klassifikation=klassifikation, land=land)

    return render(request, 'arkiveringsversioner/import.html', {
    })

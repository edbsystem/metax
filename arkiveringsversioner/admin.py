from django.contrib import admin

from .models import Leverandoer, Type, Arkiveringsversion, Status, Version, Helligdag


class LeverandoerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'navn',)
    ordering = ['navn']


class TypeAdmin(admin.ModelAdmin):
    list_display = ('navn',)
    ordering = ['navn']


class ArkiveringsversionAdmin(admin.ModelAdmin):
    list_display = ('avid', 'jnr', 'titel', 'kategori', 'klassifikation', 'type', 'land', 'public')
    ordering = ['avid']


class StatusAdmin(admin.ModelAdmin):
    list_display = ('navn',)
    ordering = ['navn']


class VersionAdmin(admin.ModelAdmin):
    list_display = ('nummer', 'avid', 'tester', 'arkivar', 'modtaget', 'svar')
    ordering = ['nummer']


class HelligdagAdmin(admin.ModelAdmin):
    list_display = ('dag',)
    ordering = ['dag']


admin.site.register(Leverandoer, LeverandoerAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Arkiveringsversion, ArkiveringsversionAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(Helligdag, HelligdagAdmin)

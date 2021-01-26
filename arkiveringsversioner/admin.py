from django.contrib import admin

from .models import Leverandoer, Type, Arkiveringsversion, Status, Version


class LeverandoerAdmin(admin.ModelAdmin):
    list_display = ('navn',)
    ordering = ['navn']


class TypeAdmin(admin.ModelAdmin):
    list_display = ('navn',)
    ordering = ['navn']


class ArkiveringsversionAdmin(admin.ModelAdmin):
    list_display = ('avid', 'jnr', 'titel')
    ordering = ['avid']


class StatusAdmin(admin.ModelAdmin):
    list_display = ('navn',)
    ordering = ['navn']


class VersionAdmin(admin.ModelAdmin):
    list_display = ('nummer', 'avid')
    ordering = ['nummer']


admin.site.register(Leverandoer, LeverandoerAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Arkiveringsversion, ArkiveringsversionAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Version, VersionAdmin)

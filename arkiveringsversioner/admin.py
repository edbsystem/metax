from django.contrib import admin

from .models import Leverandoer, Type, Arkiveringsversion, Status


class LeverandoerAdmin(admin.ModelAdmin):
    list_display = ('navn',)
    ordering = ['navn']


class TypeAdmin(admin.ModelAdmin):
    list_display = ('navn',)
    ordering = ['navn']


class ArkiveringsversionAdmin(admin.ModelAdmin):
    list_display = ('avid', 'version', 'jnr', 'titel')
    ordering = ['avid', 'version']


class StatusAdmin(admin.ModelAdmin):
    list_display = ('navn',)
    ordering = ['navn']


admin.site.register(Leverandoer, LeverandoerAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Arkiveringsversion, ArkiveringsversionAdmin)
admin.site.register(Status, StatusAdmin)

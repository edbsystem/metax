from django.contrib import admin

from .models import Medie, Placering, Maskine


class MedieAdmin(admin.ModelAdmin):
    list_display = ('navn',)
    ordering = ['navn']


class PlaceringAdmin(admin.ModelAdmin):
    list_display = ('lokation', 'lokale')
    ordering = ['lokation', 'lokale']


class MaskineAdmin(admin.ModelAdmin):
    list_display = ('navn',)
    ordering = ['navn']


admin.site.register(Medie, MedieAdmin)
admin.site.register(Placering, PlaceringAdmin)
admin.site.register(Maskine, MaskineAdmin)

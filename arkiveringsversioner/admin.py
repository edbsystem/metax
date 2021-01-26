from django.contrib import admin

from .models import Leverandoer, Type


class LeverandoerAdmin(admin.ModelAdmin):
    list_display = ('navn',)
    ordering = ['navn']


class TypeAdmin(admin.ModelAdmin):
    list_display = ('navn',)
    ordering = ['navn']


admin.site.register(Leverandoer, LeverandoerAdmin)
admin.site.register(Type, TypeAdmin)

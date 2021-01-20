from django.contrib import admin

from .models import Leverandoer


class LeverandoerAdmin(admin.ModelAdmin):
    list_display = ('navn',)
    ordering = ['navn']


admin.site.register(Leverandoer, LeverandoerAdmin)

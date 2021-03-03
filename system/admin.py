from django.contrib import admin

from .models import Profil, Bruger, Gruppe, Rettighed, Titel


class ProfilAdmin(admin.ModelAdmin):
    list_display = ('initialer', 'titel')
    ordering = ['initialer']


class BrugerAdmin(admin.ModelAdmin):
    list_display = ('profil',)
    ordering = ['profil']


class GruppeAdmin(admin.ModelAdmin):
    list_display = ('navn',)
    ordering = ['navn']


class RettighedAdmin(admin.ModelAdmin):
    list_display = ('navn',)
    ordering = ['navn']


class TitelAdmin(admin.ModelAdmin):
    list_display = ('navn',)
    ordering = ['navn']


admin.site.register(Profil, ProfilAdmin)
admin.site.register(Bruger, BrugerAdmin)
admin.site.register(Gruppe, GruppeAdmin)
admin.site.register(Rettighed, RettighedAdmin)
admin.site.register(Titel, TitelAdmin)

from django.urls import path

from .views import system_view, profil_view

urlpatterns = [
    path('', system_view, name='system_view'),

    path('profil/', profil_view, name='profil_view'),
]

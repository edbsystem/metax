from django.urls import path

from .views import arkiveringsversioner_view, leverandoerer_view, typer_view, leverandoer_view

urlpatterns = [
    path('', arkiveringsversioner_view, name='arkiveringsversioner_view'),


    path('leverandoerer/', leverandoerer_view, name='leverandoerer_view'),
    path('leverandoer/', leverandoer_view, name='leverandoer_view'),
    path('leverandoer/<str:pk>/', leverandoer_view, name='leverandoer_view'),


    path('typer/', typer_view, name='typer_view'),
    #path('typer/', medie_view, name='typer_view'),
    #path('typer/<str:pk>/', medie_view, name='typer_view'),

]

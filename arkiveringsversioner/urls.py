from django.urls import path

from .views import arkiveringsversioner_view, leverandoerer_view, typer_view, leverandoer_view, type_view, arkiveringsversion_view, soeg_view, import_view

urlpatterns = [
    path('', arkiveringsversioner_view, name='arkiveringsversioner_view'),

    path('arkiveringsversion/<str:avid>/', arkiveringsversion_view, name='arkiveringsversion_view'),
    path('arkiveringsversion/<str:avid>/<str:version>/', arkiveringsversion_view, name='arkiveringsversion_view'),
    path('arkiveringsversion/<str:avid>/<str:version>/<str:nystatus>/', arkiveringsversion_view, name='arkiveringsversion_view'),

    path('soeg/', soeg_view, name='soeg_view'),
    path('import/', import_view, name='import_view'),

    path('leverandoerer/', leverandoerer_view, name='leverandoerer_view'),
    path('leverandoer/', leverandoer_view, name='leverandoer_view'),
    path('leverandoer/<str:pk>/', leverandoer_view, name='leverandoer_view'),

    path('typer/', typer_view, name='typer_view'),
    path('type/', type_view, name='type_view'),
    path('type/<str:pk>/', type_view, name='type_view'),

]

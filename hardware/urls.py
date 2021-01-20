from django.urls import path

from .views import hardware_view, maskiner_view, maskine_view, medier_view, medie_view

urlpatterns = [
    path('', hardware_view, name='hardware_view'),


    path('maskiner/', maskiner_view, name='maskiner_view'),
    path('maskine/', maskine_view, name='maskine_view'),
    path('maskine/<str:pk>/', maskine_view, name='maskine_view'),


    path('medier/', medier_view, name='medier_view'),
    path('medie/', medie_view, name='medie_view'),
    path('medie/<str:pk>/', medie_view, name='medie_view'),


]

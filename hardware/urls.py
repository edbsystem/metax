from django.urls import path

from .views import hardware_view

urlpatterns = [
    path('', hardware_view, name='hardware_view'),
]

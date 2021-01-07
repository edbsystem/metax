from django.urls import path

from .views import forside_view

urlpatterns = [
    path('', forside_view, name='forside_view'),
]

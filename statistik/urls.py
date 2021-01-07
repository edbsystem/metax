from django.urls import path

from .views import statistik_view

urlpatterns = [
    path('', statistik_view, name='statistik_view'),
]

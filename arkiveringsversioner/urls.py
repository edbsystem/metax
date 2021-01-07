from django.urls import path

from .views import arkiveringsversioner_view

urlpatterns = [
    path('', arkiveringsversioner_view, name='arkiveringsversioner_view'),
]

from django.urls import path
from django.contrib.auth import views as auth_views

from .views import system_view, profil_view, profil_save, brugere_view, grupper_view

urlpatterns = [
    path('logind/', auth_views.LoginView.as_view(template_name='login.html'), name='login_view'),
    path('logud/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout_view'),

    path('', system_view, name='system_view'),

    path('profil/', profil_view, name='profil_view'),

    path('brugere/', brugere_view, name='brugere_view'),

    path('grupper/', grupper_view, name='grupper_view'),
]

from django.urls import path
from django.contrib.auth import views as auth_views

from .views import system_view, profil_view, profil_save

urlpatterns = [
    path('logind/', auth_views.LoginView.as_view(template_name='login.html'), name='login_view'),
    path('logud/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout_view'),

    path('', system_view, name='system_view'),

    path('profil/', profil_view, name='profil_view'),
    path('profil_gem/', profil_save, name='profil_save'),
]

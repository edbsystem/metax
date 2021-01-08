from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test

from system.models import Profil, Bruger, Gruppe
from system.services import rettigheder, tjek_rettigheder


def tjek(user):
    return tjek_rettigheder(user, {'system_gruppe_se'})


@ user_passes_test(tjek, login_url='/', redirect_field_name=None)
def gruppe_view(request, navn=None):
    pass

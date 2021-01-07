from django.shortcuts import render


def hardware_view(request):
    return render(request, 'hardware.html')

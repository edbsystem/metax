from django.shortcuts import render


def system_view(request):
    return render(request, 'system.html')

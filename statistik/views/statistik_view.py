from django.shortcuts import render


def statistik_view(request):
    return render(request, 'statistik.html')

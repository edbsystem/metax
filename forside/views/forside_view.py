from django.shortcuts import render


def forside_view(request):
    return render(request, 'forside.html')

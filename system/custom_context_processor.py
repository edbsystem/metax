from django.db.models.functions import Lower

from system.models import Gruppe


def subject_renderer(request):

    _grupper = []
    for gruppe in Gruppe.objects.all().order_by(Lower('navn')):
        _grupper.append(gruppe.navn)

    return {
        "grupper": _grupper,
    }

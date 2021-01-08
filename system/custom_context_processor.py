from django.db.models.functions import Lower

from system.models import Gruppe, Rettighed


def subject_renderer(request):

    _grupper = []
    for gruppe in Gruppe.objects.all().order_by(Lower('navn')):
        _grupper.append(gruppe.navn)

    _rettigheder = []
    for rettighed in list(Rettighed._meta.get_field('navn').choices):
        _rettigheder.append(rettighed[1])

    return {
        "grupper": _grupper,
        "rettigheder": _rettigheder,
    }

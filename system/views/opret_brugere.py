from django.contrib.auth.models import User
from system.models import Profil, Bruger, Gruppe

testere = {4: 'THH', 5: 'IHA', 6: 'SLL', 7: 'NRS', 8: 'BGJ', 9: 'PMT', 10: 'JDS', 11: 'ABN', 12: 'REM', 13: 'AKE', 14: 'IGC', 15: 'FHK', 16: 'ASS', 17: 'TBO', 18: 'PBP', 19: 'USN', 20: 'KVG', 21: 'STL', 23: 'LUK', 24: 'IHL', 25: 'CBM'}

for pk, initialer in testere.items():
    User.objects.create_user(pk=pk, username=initialer)
    profil_obj = Profil.objects.create(initialer=initialer)
    bruger_obj = Bruger.objects.create(profil=profil_obj)

from apps.atlets.models import PerguruanProfil


def perguruan(request):
    try:
        profil = PerguruanProfil.objects.first()
    except Exception:
        profil = None
    return {'perguruan_global': profil}

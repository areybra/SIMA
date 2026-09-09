from django.shortcuts import redirect


def landing(request):
    """Root URL langsung jadi pintu login.

    Fitur landing publik (tentang, berita, prestasi, kontak) dihapus.
    - Anonim -> /login/
    - Sudah login -> /dashboard/ (router by role)
    """
    if request.user.is_authenticated:
        return redirect('dashboard-router')
    return redirect('login')

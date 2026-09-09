from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def strict_role_required(*allowed_roles):
    """Batasi view berdasarkan CustomUser.role saja, tanpa pengecualian.

    Superuser TIDAK otomatis lolos. Dipakai agar akun admin terisolasi
    penuh dari dashboard (admin hanya beraktivitas di /admin/).

    Contoh: @strict_role_required('pelatih').
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            if getattr(request.user, 'role', None) in allowed_roles:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied('Anda tidak memiliki akses ke halaman ini.')
        return _wrapped
    return decorator


pelatih_required = strict_role_required('pelatih')
atlet_required = strict_role_required('atlet')

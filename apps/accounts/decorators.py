from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def role_required(*allowed_roles):
    """Batasi view berdasarkan CustomUser.role.

    Contoh: @role_required('admin', 'pelatih').
    Superuser selalu lolos.
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if user.is_superuser:
                return view_func(request, *args, **kwargs)
            if getattr(user, 'role', None) in allowed_roles:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied('Anda tidak memiliki akses ke halaman ini.')
        return _wrapped
    return decorator


admin_pelatih_required = role_required('admin', 'pelatih')
jurnalis_required = role_required('admin', 'jurnalis')
admin_pelatih_jurnalis_required = role_required('admin', 'pelatih', 'jurnalis')

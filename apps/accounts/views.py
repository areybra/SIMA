from django import forms
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView

from .ratelimit import bump_rate_limit, check_rate_limit, clear_rate_limit


class SIMALoginView(LoginView):
    """Halaman login khusus pelatih/atlet.

    Akun admin (role admin / superuser) ditolak di sini dan diarahkan
    untuk login melalui /admin/ saja.
    """

    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            blocked = check_rate_limit(request, key_prefix='login')
            if blocked is not None:
                return blocked
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        if user.is_superuser or getattr(user, 'role', '') == 'admin':
            logout(self.request)
            # Samarkan: pakai pesan invalid_login bawaan Django yang sama
            # persis seperti password salah, agar tidak membocorkan URL /admin/.
            form.add_error(
                None,
                forms.ValidationError(
                    form.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': form.username_field.verbose_name},
                ),
            )
            bump_rate_limit(self.request, key_prefix='login')
            return self.form_invalid(form)
        clear_rate_limit(self.request, key_prefix='login')
        return super().form_valid(form)

    def form_invalid(self, form):
        bump_rate_limit(self.request, key_prefix='login')
        return super().form_invalid(form)

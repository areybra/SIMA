from django import forms

from .models import CustomUser


class AccountProfileForm(forms.ModelForm):
    """Form pengaturan akun milik sendiri (bukan profil data atlet).

    Role / status staff tidak bisa diubah dari sini — hanya admin via /admin/.
    """

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'no_hp']
        labels = {
            'username': 'Username',
            'first_name': 'Nama depan',
            'last_name': 'Nama belakang',
            'email': 'Email',
            'no_hp': 'No. HP / WA',
        }
        help_texts = {
            'username': 'Dipakai untuk login. Huruf, angka, dan @/./+/-/_ saja.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'

from django import forms

from .models import AtletProfile, Cabor, DokumenAtlet, PerguruanProfil, Prestasi


class BootstrapMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get('class', '')
            if isinstance(field.widget, (forms.CheckboxInput,)):
                field.widget.attrs['class'] = f'{css} form-check-input'.strip()
            else:
                field.widget.attrs['class'] = f'{css} form-control'.strip()


class CaborForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Cabor
        fields = ['nama', 'deskripsi', 'aktif']


class PerguruanProfilForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = PerguruanProfil
        fields = ['nama', 'tentang', 'visi', 'misi', 'alamat', 'kontak', 'logo']


class AtletProfileForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = AtletProfile
        fields = [
            'user', 'nama_lengkap', 'jenis_kelamin', 'tempat_lahir', 'tanggal_lahir',
            'cabor', 'kelas_kategori', 'tahun_masuk', 'tinggi_cm', 'berat_kg',
            'status_aktif', 'foto', 'no_hp', 'alamat',
        ]
        widgets = {'tanggal_lahir': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.accounts.models import CustomUser
        self.fields['user'].queryset = CustomUser.objects.filter(role=CustomUser.Roles.ATLET)
        self.fields['user'].required = False


class PrestasiForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Prestasi
        fields = ['atlet', 'nama_kejuaraan', 'tingkat', 'hasil', 'tahun', 'bukti']


class DokumenAtletForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = DokumenAtlet
        fields = ['atlet', 'label', 'file', 'keterangan']
        widgets = {'label': forms.TextInput(attrs={'placeholder': 'Contoh: KTP / KK / Akta Kelahiran / Ijazah'})}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Atlet: atlet field dikunci ke profilnya sendiri
        if user and getattr(user, 'role', None) == 'atlet' and hasattr(user, 'atlet_profile') and user.atlet_profile:
            self.fields['atlet'].queryset = AtletProfile.objects.filter(pk=user.atlet_profile.pk)
            self.fields['atlet'].initial = user.atlet_profile
            self.fields['atlet'].widget.attrs['readonly'] = True

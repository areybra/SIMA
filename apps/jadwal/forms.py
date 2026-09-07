from django import forms

from .models import AgendaEvent, JadwalLatihan


class JadwalLatihanForm(forms.ModelForm):
    class Meta:
        model = JadwalLatihan
        fields = ['cabor', 'hari', 'jam_mulai', 'jam_selesai', 'lokasi', 'pelatih', 'kelompok', 'keterangan', 'aktif']
        widgets = {
            'jam_mulai': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'jam_selesai': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


class AgendaEventForm(forms.ModelForm):
    class Meta:
        model = AgendaEvent
        fields = ['nama', 'jenis', 'tanggal_mulai', 'tanggal_selesai', 'lokasi', 'cabor', 'deskripsi']
        widgets = {
            'tanggal_mulai': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tanggal_selesai': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'

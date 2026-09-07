from django import forms

from .models import PenilaianKesiapan


class PenilaianKesiapanForm(forms.ModelForm):
    class Meta:
        model = PenilaianKesiapan
        fields = [
            'atlet', 'tanggal', 'fisik', 'teknik', 'mental', 'vo2max',
            'berat_kg', 'tinggi_cm', 'kehadiran', 'ada_cedera',
            'keterangan_cedera', 'catatan_pelatih',
        ]
        widgets = {'tanggal': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = field.widget.attrs.get('class', '')
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = f'{css} form-check-input'.strip()
            elif 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'

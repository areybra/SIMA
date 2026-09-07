from django import forms

from .models import Berita, ContactMessage


class BeritaForm(forms.ModelForm):
    class Meta:
        model = Berita
        fields = ['judul', 'kategori', 'ringkasan', 'konten', 'cover', 'is_published', 'is_featured']
        widgets = {
            'konten': forms.Textarea(attrs={'rows': 12, 'class': 'form-control richtext', 'placeholder': 'Tulis berita dengan format: heading, Tebal, Miring, List, Link, Gambar... (mendukung HTML)' }),
            'ringkasan': forms.TextInput(attrs={'placeholder': 'Ringkasan singkat untuk kartu & landing (maks 300)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif name != 'konten' and 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['nama', 'email', 'subjek', 'pesan']
        widgets = {
            'pesan': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Tulis pesan Anda...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'

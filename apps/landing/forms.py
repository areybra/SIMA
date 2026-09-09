from django import forms

from .models import ContactMessage


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

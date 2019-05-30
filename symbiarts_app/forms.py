from django import forms

from .models import Obra, ObraArchivo


class ObraForm(forms.ModelForm):

    class Meta:
        model = Obra
        fields = (
            'nombre',
            'descripcion',
            'stock',
            'estado',
            'dimensiones',
            'precio',
            'tipo',)


class ObraArchivosForm(forms.ModelForm):
    class Meta:
        model = ObraArchivo
        fields = ['archivo']
        widgets = {
            'archivo': forms.ClearableFileInput(
                attrs={'multiple': True, 'required': True}),
        }

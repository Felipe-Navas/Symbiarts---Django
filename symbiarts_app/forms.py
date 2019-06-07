from django import forms

from .models import Comentario, Obra, ObraArchivo


class FormObra(forms.ModelForm):

    class Meta:
        model = Obra
        fields = (
            'nombre',
            'categoria',
            'descripcion',
            'stock',
            'estado',
            'dimensiones',
            'precio',
            'tipo',)


class FormObraArchivos(forms.ModelForm):
    class Meta:
        model = ObraArchivo
        fields = ['archivo']
        widgets = {
            'archivo': forms.ClearableFileInput(
                attrs={'multiple': True, 'required': True}),
        }


class FormComentario(forms.ModelForm):

    class Meta:
        model = Comentario
        fields = ('texto',)

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
        fields = ['texto']
        widgets = {
          'texto': forms.Textarea(attrs={'rows': 2}),
        }


class FormBuscar(forms.Form):
    cadena = forms.CharField(max_length=50)


class FormComoPagarObra(forms.Form):
    metodoPago = forms.CharField(widget=forms.HiddenInput, required=False)

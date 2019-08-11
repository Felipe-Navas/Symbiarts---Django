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

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get("tipo")
        precio = cleaned_data.get("precio")
        stock = cleaned_data.get("stock")

        if tipo == 'AS':
            if not precio or precio <= 0:
                self.add_error("precio",
                               "Ingresar correctamente el precio de la obra!")
            if stock <= 0:
                self.add_error("stock",
                               "Ingresar correctamente el stock de la obra!")


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

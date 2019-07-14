from django import forms


class FormAgregarObraCarrito(forms.Form):
    def __init__(self, *args, **kwargs):
        stock = kwargs.pop('stock')
        lista_stock = [(i, str(i)) for i in range(1, stock+1)]
        super(FormAgregarObraCarrito, self).__init__(*args, **kwargs)
        self.fields['cantidad'] = forms.TypedChoiceField(
            choices=lista_stock, coerce=int)

    cantidad = forms.TypedChoiceField()

    actualizar_cantidad = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput)

    accion = forms.CharField(widget=forms.HiddenInput, required=False)

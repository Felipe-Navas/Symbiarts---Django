from django import forms


# Reemplazar por el stock del producto
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 26)]


class FormAgregarObraCarrito(forms.Form):
    cantidad = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES, coerce=int)

    actualizar_cantidad = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput)

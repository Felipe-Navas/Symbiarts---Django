from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from symbiarts_app.models import Obra
from .carrito import Carrito
from .forms import FormAgregarObraCarrito


@require_POST
def agregar_obra_carrito(request, obra_id):
    carrito = Carrito(request)
    obra = get_object_or_404(Obra, id=obra_id)
    form = FormAgregarObraCarrito(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        carrito.agregar_obra(
            obra=obra,
            cantidad=cd['cantidad'],
            actualizar_cantidad=cd['actualizar_cantidad']
            )
    return redirect('carrito:detalle_carrito')


def eliminar_obra_carrito(request, obra_id):
    carrito = Carrito(request)
    obra = get_object_or_404(Obra, id=obra_id)
    carrito.eliminar_obra(obra)
    return redirect('carrito:detalle_carrito')


def detalle_carrito(request):
    carrito = Carrito(request)
    for item in carrito:
        item['form_agregar_obra_carrito'] = FormAgregarObraCarrito(
            initial={'cantidad': item['cantidad'], 'actualizar_cantidad': True}
            )
    return render(request, 'carrito/detalle_carrito.html', {
        'carrito': carrito
        })

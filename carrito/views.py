from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from symbiarts_app.models import Obra
from symbiarts_app.forms import FormBuscar
from .carrito import Carrito
from .forms import FormAgregarObraCarrito


@require_POST
def agregar_obra_carrito(request, obra_id):
    carrito = Carrito(request)
    obra = get_object_or_404(Obra, id=obra_id)

    if request.user == obra.usuario:
        mensaje = ("no puede agregar al carrito esta obra porque le pertenece"
                   " a usted mismo!.")
        return render(request, 'symbiarts_app/error_generico.html', {
            'mensaje': mensaje})

    if obra.tipo == 'AW':
        mensaje = ("no puede agregar al carrito esta obra porque es de tipo"
                   " ArtWork.")
        return render(request, 'symbiarts_app/error_generico.html', {
            'mensaje': mensaje})

    if obra.pausada:
        mensaje = ("no puede agregar al carrito esta obra porque esta "
                   "pausada.")
        return render(request, 'symbiarts_app/error_generico.html', {
            'mensaje': mensaje})

    form = FormAgregarObraCarrito(request.POST,
                                  stock=obra.obtener_stock())
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
        stock = item['obra'].stock
        formAgregarObraCarrito = FormAgregarObraCarrito(
            stock=stock)
        formAgregarObraCarrito.fields['cantidad'].initial = item['cantidad']
        formAgregarObraCarrito.fields['actualizar_cantidad'].initial = True
        item['form_agregar_obra_carrito'] = formAgregarObraCarrito
    formBuscar = FormBuscar()
    return render(request, 'carrito/detalle_carrito.html', {
        'carrito': carrito,
        'formBuscar': formBuscar})

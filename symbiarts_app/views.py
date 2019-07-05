from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from .models import (Obra, ObraArchivo, Comentario, MetodoPago, VentaObra,
                     DetalleVentaObra)
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import (FormObra, FormObraArchivos, FormComentario, FormBuscar,
                    FormComoPagarObra)
from carrito.forms import FormAgregarObraCarrito
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from carrito.carrito import Carrito


def lista_obras(request):
    queryset = Obra.objects.filter(
        fecha_publicacion__lte=timezone.now()).order_by('-fecha_publicacion')
    page = request.GET.get('page')
    paginator = Paginator(queryset, 21)
    try:
        obras = paginator.page(page)
    except PageNotAnInteger:
        # Volver a la primera página
        obras = paginator.page(1)
    except EmptyPage:
        # Voy a la ultima página si llega una inexistente
        obras = paginator.page(paginator.num_pages)
    formBuscar = FormBuscar()
    return render(request, 'symbiarts_app/lista_obras.html', {
        'obras': obras,
        'formBuscar': formBuscar})


def detalle_obra(request, pk):
    obra = get_object_or_404(Obra, pk=pk)
    archivos_obra = ObraArchivo.objects.filter(obra__pk=pk)

    queryset = obra.comentarios.all()
    page = request.GET.get('page')
    paginator = Paginator(queryset, 10)
    try:
        comentarios = paginator.page(page)
    except PageNotAnInteger:
        # Volver a la primera página
        comentarios = paginator.page(1)
    except EmptyPage:
        # Voy a la ultima página si llega una inexistente
        comentarios = paginator.page(paginator.num_pages)

    formComentario = FormComentario()
    formCarrito = FormAgregarObraCarrito()
    formBuscar = FormBuscar()
    return render(request, 'symbiarts_app/detalle_obra.html', {
        'obra': obra,
        'archivos_obra': archivos_obra,
        'formComentario': formComentario,
        'comentarios': comentarios,
        'formCarrito': formCarrito,
        'formBuscar': formBuscar})


@login_required
def nueva_obra(request):
    if request.method == "POST":
        form = FormObra(request.POST)
        file_form = FormObraArchivos(request.POST, request.FILES)
        files = request.FILES.getlist('archivo')
        if form.is_valid() and file_form.is_valid():
            obra = form.save(commit=False)
            obra.usuario = request.user
            obra.save()
            for f in files:
                obra_archivo = ObraArchivo(archivo=f, obra=obra)
                obra_archivo.save()
            return redirect('symbiarts_app:detalle_obra', pk=obra.pk)
    else:
        form = FormObra()
        file_form = FormObraArchivos()
    es_nueva_obra = True
    return render(request, 'symbiarts_app/editar_obra.html', {
        'form': form,
        'file_form': file_form,
        'es_nueva_obra': es_nueva_obra})


@login_required
def editar_obra(request, pk):
    obra = get_object_or_404(Obra, pk=pk)
#    obra_archivo = ObraArchivo.objects.filter(obra__pk=pk)
    if request.method == "POST":
        form = FormObra(request.POST, instance=obra)
        file_form = FormObraArchivos(
            request.POST,
            request.FILES,
            instance=obra)
        files = request.FILES.getlist('archivo')
        if form.is_valid() and file_form.is_valid():
            obra = form.save(commit=False)
            obra.id_usuario = request.user
            obra.save()
            # Ver si borro to lo que tiene relacionado el ObraArchivos
            for f in files:
                obra_archivo = ObraArchivo(archivo=f, obra=obra)
                obra_archivo.save()
            return redirect('symbiarts_app:detalle_obra', pk=obra.pk)
    else:
        form = FormObra(instance=obra)
#        file_form = FormObraArchivos(instance=obra_archivo)
        file_form = FormObraArchivos()
    es_nueva_obra = False
    return render(request, 'symbiarts_app/editar_obra.html', {
        'form': form,
        'file_form': file_form,
        'es_nueva_obra': es_nueva_obra})


@login_required
def eliminar_obra(request, pk):
    obra = get_object_or_404(Obra, pk=pk)
    obra.delete()
    return redirect('symbiarts_app:lista_obras')


@login_required
def nuevo_comentario(request, pk):
    obra = get_object_or_404(Obra, pk=pk)
    if request.method == "POST":
        form = FormComentario(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.obra = obra
            comentario.usuario = request.user
            comentario.save()
            return redirect('symbiarts_app:detalle_obra', pk=obra.pk)
    else:
        return redirect('symbiarts_app:detalle_obra', pk=obra.pk)


@login_required
def eliminar_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    comentario.delete()
    return redirect('symbiarts_app:detalle_obra',
                    pk=comentario.obra.pk)


queryset_buscar = None
cadena_buscada = None


def buscar_obras(request):
    if request.method == "POST":
        formBuscar = FormBuscar(request.POST)
        if formBuscar.is_valid():
            global cadena_buscada
            cadena_buscada = formBuscar.cleaned_data.get("cadena")
            lookups = ((Q(nombre__icontains=cadena_buscada) |
                       Q(descripcion__icontains=cadena_buscada) |
                       Q(categoria__nombre__icontains=cadena_buscada)) &
                       Q(fecha_publicacion__lte=timezone.now()))
            global queryset_buscar
            queryset_buscar = Obra.objects.filter(
                lookups).order_by('-fecha_publicacion')

    page = request.GET.get('page')
    paginator = Paginator(queryset_buscar, 21)
    try:
        obras = paginator.page(page)
    except PageNotAnInteger:
        # Volver a la primera página
        obras = paginator.page(1)
    except EmptyPage:
        # Voy a la ultima página si llega una inexistente
        obras = paginator.page(paginator.num_pages)
    formBuscar = FormBuscar()

    return render(request, 'symbiarts_app/lista_obras.html', {
        'obras': obras,
        'formBuscar': formBuscar,
        'cadena_buscada': cadena_buscada})


@require_POST
def orquestar_compra_carrito(request, obra_id):
    formCarrito = FormAgregarObraCarrito(request.POST)
    if formCarrito.is_valid():
        cantidad_obras = formCarrito.cleaned_data.get("cantidad")
        metodos_pago = MetodoPago.objects.order_by('nombre')
        obra = get_object_or_404(Obra, pk=obra_id)
        accion = formCarrito.cleaned_data.get("accion")
        if accion == 'comprar':
            request.session['cantidad_obras'] = cantidad_obras
            formComoPagarObra = FormComoPagarObra()
            return render(request, 'symbiarts_app/como_pagar_obra.html', {
                'obra': obra,
                'metodos_pago': metodos_pago,
                'cantidad_obras': cantidad_obras,
                'formComoPagarObra': formComoPagarObra})
        elif accion == 'agregar_al_carrito':
            carrito = Carrito(request)
            act_cantidad = formCarrito.cleaned_data.get('actualizar_cantidad')
            carrito.agregar_obra(
                obra=obra,
                cantidad=cantidad_obras,
                actualizar_cantidad=act_cantidad
                )
            return redirect('carrito:detalle_carrito')


@require_POST
def confirmar_compra(request, obra_id):
    obra = get_object_or_404(Obra, id=obra_id)
    formComoPagarObra = FormComoPagarObra(request.POST)
    if formComoPagarObra.is_valid():
        metodo_pago_elegido = formComoPagarObra.cleaned_data.get('metodoPago')
        request.session['metodo_pago_elegido'] = metodo_pago_elegido
        cantidad_obras = request.session['cantidad_obras']
        return render(request, 'symbiarts_app/confirmar_compra.html', {
            'obra': obra,
            'cantidad_obras': cantidad_obras})


@login_required
@require_POST
def grabar_compra(request, obra_id):
    obra = get_object_or_404(Obra, id=obra_id)
    metodo_pago_elegido = request.session['metodo_pago_elegido']
    cantidad_obras = request.session['cantidad_obras']
    metodo_pago = MetodoPago.objects.filter(nombre=metodo_pago_elegido).first()
    venta_obra = VentaObra.objects.create(
        cliente=request.user,
        metodo_pago=metodo_pago)

    DetalleVentaObra.objects.create(
        venta_obra=venta_obra,
        obra=obra,
        precio_obra=obra.precio,
        cantidad_obra=cantidad_obras)
    request.session['compra_exitosa'] = True
    return redirect('symbiarts_app:compra_exitosa')


@login_required
def compra_exitosa(request):
    if request.session['compra_exitosa'] == True:
        request.session['compra_exitosa'] = False
        return render(request, 'symbiarts_app/compra_exitosa.html')
    else:
        return redirect('symbiarts_app:lista_obras')

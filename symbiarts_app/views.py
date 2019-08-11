from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from .models import (Obra, ObraArchivo, Comentario, VentaObra,
                     DetalleVentaObra)
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import (FormObra, FormObraArchivos, FormComentario, FormBuscar)
from carrito.forms import FormAgregarObraCarrito
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from carrito.carrito import Carrito
from django.conf import settings
import mercadopago
import json
from decimal import Decimal
import datetime
import time


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
    formCarrito = FormAgregarObraCarrito(stock=obra.obtener_stock())
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
    if request.user != obra.usuario:
        mensaje = ("Estimado/a, {}, no puede editar esta obra porque le "
                   "pertenece a otro usuario.").format(request.user.username)
        return render(request, 'symbiarts_app/error_generico.html', {
            'mensaje': mensaje
            })
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
def pausar_obra(request, pk):
    obra = get_object_or_404(Obra, pk=pk)
    if request.user == obra.usuario:
        obra.pausada = True
        obra.fecha_pausada = timezone.now()
        obra.save()
        return redirect('symbiarts_app:detalle_obra', pk=obra.pk)
    else:
        mensaje = ("Estimado/a, {}, no puede pausar esta obra porque le "
                   "pertenece a otro usuario.").format(request.user.username)
        return render(request, 'symbiarts_app/error_generico.html', {
            'mensaje': mensaje
            })


@login_required
def reactivar_obra(request, pk):
    obra = get_object_or_404(Obra, pk=pk)
    if request.user == obra.usuario:
        obra.pausada = False
        obra.fecha_pausada = None
        obra.save()
        return redirect('symbiarts_app:detalle_obra', pk=obra.pk)
    else:
        mensaje = ("Estimado/a, {}, no puede reactivar esta obra porque le "
                   "pertenece a otro usuario.").format(request.user.username)
        return render(request, 'symbiarts_app/error_generico.html', {
            'mensaje': mensaje
            })


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
    if request.user != comentario.usuario:
        mensaje = ("Estimado/a, {}, no puede eliminar este comentario porque "
                   " le pertenece a otro usuario.").format(
                   request.user.username)
        return render(request, 'symbiarts_app/error_generico.html', {
            'mensaje': mensaje
            })
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
    obra = get_object_or_404(Obra, pk=obra_id)
    if request.user == obra.usuario:
        mensaje = ("Estimado/a, {}, no puede comprar esta obra porque le "
                   "pertenece a usted mismo!.").format(request.user.username)
        return render(request, 'symbiarts_app/error_generico.html', {
            'mensaje': mensaje
            })
    formCarrito = FormAgregarObraCarrito(request.POST,
                                         stock=obra.obtener_stock())
    if formCarrito.is_valid():
        cantidad_obras = formCarrito.cleaned_data.get("cantidad")
        accion = formCarrito.cleaned_data.get("accion")
        if accion == 'comprar':
            request.session['cantidad_obras'] = cantidad_obras
            precio_total = cantidad_obras * obra.precio
            preference = crear_preference_api_mercadopago(
                request, obra=obra)
            return render(request, 'symbiarts_app/confirmar_compra.html', {
                'obra': obra,
                'cantidad_obras': cantidad_obras,
                'precio_total': precio_total,
                'preference': preference,
                'public_key': settings.MP_PUBLIC_KEY})
        elif accion == 'agregar_al_carrito':
            carrito = Carrito(request)
            act_cantidad = formCarrito.cleaned_data.get('actualizar_cantidad')
            carrito.agregar_obra(
                obra=obra,
                cantidad=cantidad_obras,
                actualizar_cantidad=act_cantidad
                )
            return redirect('carrito:detalle_carrito')


@login_required
def crear_preference_api_mercadopago(request, obra):
    mp = mercadopago.MP(settings.MP_ACCESS_TOKEN)
    id_obra = str(obra.id)
    nombre_obra = obra.nombre
    descripcion = obra.descripcion
    cantidad = request.session['cantidad_obras']
    external_reference = str(obra.id)
    request.session['external_reference'] = external_reference
    precio_unitario = obra.precio
    preference = {
        "items": [
            {
                "id": id_obra,
                "title": nombre_obra,
                "description": descripcion,
                "quantity": cantidad,
                "currency_id": "ARS",
                "unit_price": 1
            }
        ],
        "back_urls": {
            "success": "http://localhost:8000",
            "failure": "http://localhost:8000/fallo",
            "pending": "http://localhost:8000/pending"
            },
        "auto_return": "approved",
        "external_reference": external_reference,
        "binary_mode": True,
    }
    """
        "payer": {
            "name": "Nombre Test",
            "surname": "Apellido",
            "email": "test_user_85852805@testuser.com",
            "identification": {
                "type": "DNI",
                "number": "12345678"
                }
            },
    """
    """ Agregar fecha de expiracion a la preference
        utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
        utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
        datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat()

        -En el json:
        "expires": True,
        "expiration_date_from": "2017-02-01T12:00:00.000-04:00",
        "expiration_date_to": "2017-02-28T12:00:00.000-04:00"
    """
    preferenceResult = mp.create_preference(preference)
    preference = preferenceResult["response"]
    print(preferenceResult)
    return preference


@login_required
def grabar_compra(request, obra_id):
    obra = get_object_or_404(Obra, id=obra_id)
    if request.user == obra.usuario:
        mensaje = ("Estimado/a, {}, no puede comprar esta obra porque le "
                   "pertenece a usted mismo!.").format(request.user.username)
        return render(request, 'symbiarts_app/error_generico.html', {
            'mensaje': mensaje
            })
    cantidad_obras = request.session['cantidad_obras']
    email_customer = "test_user_85852805@testuser.com"
    payer_id = buscar_id_customer_api_mercadopago(request, email_customer)
    if payer_id is None:
        mensaje = ("Estimado/a, {}, no pudimos encontrar su numero de cliente"
                   " en mercadopago, por favor intente nuevamente."
                   ).format(request.user.username)
        return render(request, 'symbiarts_app/error_generico.html', {
            'mensaje': mensaje
            })
    print(payer_id)
    external_reference = request.session['external_reference']
    id_pago = buscar_pago_api_mercadopago(request, external_reference, payer_id)
    if id_pago is None:
        mensaje = ("Estimado/a, {}, no pudimos encontrar el pago realizado"
                   " en mercadopago, por favor intente nuevamente."
                   ).format(request.user.username)
        return render(request, 'symbiarts_app/error_generico.html', {
            'mensaje': mensaje
            })
    print("payer_id" + id_pago)
    """
    venta_obra = VentaObra.objects.create(
        cliente=request.user,
        metodo_pago='Mercadopago')

    DetalleVentaObra.objects.create(
        venta_obra=venta_obra,
        obra=obra,
        precio_obra=obra.precio,
        cantidad_obra=cantidad_obras)
    obra.stock -= cantidad_obras
    obra.save()
    """
    request.session['compra_exitosa'] = True
    # return redirect('symbiarts_app:compra_exitosa', nro_compra=venta_obra.id)
    return redirect('symbiarts_app:compra_exitosa', nro_compra=999999)


@login_required
def buscar_id_customer_api_mercadopago(request, email_customer):
    mp = mercadopago.MP(settings.MP_ACCESS_TOKEN)
    customer = mp.get("/v1/customers/search", {"email": email_customer})
    print("Customer:")
    print(customer)
    if customer["response"]["results"]:
        id_customer = customer["response"]["results"][0]["id"]
    else:
        customer = crear_customer_api_mercadopago(request, email_customer)
        id_customer = customer["id"]
    return id_customer


def crear_customer_api_mercadopago(request, email_customer):
    mp = mercadopago.MP(settings.MP_ACCESS_TOKEN)
    response = mp.post("/v1/customers", {"email": email_customer})
    return response["response"]


@login_required
def buscar_pago_api_mercadopago(request, external_reference, payer_id):
    mp = mercadopago.MP(settings.MP_ACCESS_TOKEN)
    payment_data = {
        'payer.id': payer_id,
        "external_reference": external_reference
    }
    searchResult = mp.get("/v1/payments/search", payment_data)
    if searchResult["response"]["results"]:
        ultimoElemento = searchResult["response"]["results"].pop()
        print("Ultimo elemento:")
        print(ultimoElemento)
        id_pago = ultimoElemento["id"]
    else:
        id_pago = None
    return id_pago


@login_required
def compra_exitosa(request, nro_compra):
    if request.session['compra_exitosa'] == True:
        request.session['compra_exitosa'] = False
        return render(request, 'symbiarts_app/compra_exitosa.html', {
            'nro_compra': nro_compra
            })
    else:
        return redirect('symbiarts_app:lista_obras')


def comprar_carrito(request):
    carrito = Carrito(request)
    # precio_total = carrito.obtener_precio_total()
    # cantidad_obras_carrito = carrito.__len__()
    return render(request, 'symbiarts_app/confirmar_compra_carrito.html', {
        'carrito': carrito})


@login_required
def grabar_compra_carrito(request):
    carrito = request.session.get(settings.CARRITO_SESSION_ID)

    venta_obra = VentaObra.objects.create(
        cliente=request.user,
        metodo_pago='Mercadopago')

    obra_ids = carrito.keys()
    obras = Obra.objects.filter(id__in=obra_ids)
    for obra in obras:
        cantidad_obras = carrito[str(obra.id)]['cantidad']
        DetalleVentaObra.objects.create(
            venta_obra=venta_obra,
            obra=obra,
            precio_obra=obra.precio,
            cantidad_obra=cantidad_obras)
        obra.stock -= cantidad_obras
        obra.save()

    carrito.clear()
    request.session['compra_exitosa'] = True
    return redirect('symbiarts_app:compra_exitosa', nro_compra=venta_obra.id)


@login_required
def lista_compras(request):
    queryset = VentaObra.objects.filter(
        cliente=request.user).order_by('-fecha')
    page = request.GET.get('page')
    paginator = Paginator(queryset, 5)
    try:
        compras = paginator.page(page)
    except PageNotAnInteger:
        # Volver a la primera página
        compras = paginator.page(1)
    except EmptyPage:
        # Voy a la ultima página si llega una inexistente
        compras = paginator.page(paginator.num_pages)
    formBuscar = FormBuscar()
    return render(request, 'symbiarts_app/lista_compras.html', {
        'compras': compras,
        'formBuscar': formBuscar})


@login_required
def detalle_compra(request, compra_id):
    compra = get_object_or_404(VentaObra, id=compra_id)
    if request.user == compra.cliente:
        formBuscar = FormBuscar()
        return render(request, 'symbiarts_app/detalle_compra.html', {
            'compra': compra,
            'formBuscar': formBuscar})
    else:
        mensaje = ("Estimado/a, {}, no puede visualizar esta compra, porque le"
                   " pertenece a otro usuario.").format(request.user.username)
        return render(request, 'symbiarts_app/error_generico.html', {
            'mensaje': mensaje
            })


@login_required
def lista_ventas(request):
    queryset = VentaObra.objects.filter(
        detalle_venta_obra__obra__usuario=request.user).order_by(
        '-fecha').distinct()
    page = request.GET.get('page')
    paginator = Paginator(queryset, 5)
    try:
        ventas = paginator.page(page)
    except PageNotAnInteger:
        # Volver a la primera página
        ventas = paginator.page(1)
    except EmptyPage:
        # Voy a la ultima página si llega una inexistente
        ventas = paginator.page(paginator.num_pages)
    formBuscar = FormBuscar()
    return render(request, 'symbiarts_app/lista_ventas.html', {
        'ventas': ventas,
        'formBuscar': formBuscar})


@login_required
def detalle_venta(request, venta_id):
    queryset = VentaObra.objects.filter(
        detalle_venta_obra__obra__usuario=request.user, id=venta_id).distinct()
    venta = get_object_or_404(VentaObra, id=venta_id)
    if queryset:
        formBuscar = FormBuscar()
        cantidad_obras_vendedor = 0
        precio_total_vendedor = 0
        for detalle in venta.detalle_venta_obra.values():
            obra = get_object_or_404(Obra, pk=detalle['obra_id'])
            if obra.usuario == request.user:
                cantidad_obras_vendedor += detalle['cantidad_obra']
                precio_total_vendedor += Decimal(detalle['precio_obra'] *
                                                 detalle['cantidad_obra'])
        return render(request, 'symbiarts_app/detalle_venta.html', {
            'venta': venta,
            'formBuscar': formBuscar,
            'cantidad_obras_vendedor': cantidad_obras_vendedor,
            'precio_total_vendedor': precio_total_vendedor})
    else:
        mensaje = ("Estimado/a, {}, no puede visualizar esta venta, porque le"
                   " pertenece a otro usuario.").format(request.user.username)
        return render(request, 'symbiarts_app/error_generico.html', {
            'mensaje': mensaje
            })

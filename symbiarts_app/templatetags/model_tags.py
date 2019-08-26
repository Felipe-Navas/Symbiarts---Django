from django import template
from ..models import VentaObra, Obra
register = template.Library()


@register.simple_tag
def obtener_img_venta_artista(venta, artista_id):
    return VentaObra.obtener_img_venta_artista(venta, artista_id)


@register.simple_tag
def obtener_cantidad_ventas_obra(obra):
    return Obra.obtener_cantidad_ventas_obra(obra)

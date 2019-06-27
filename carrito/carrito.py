from decimal import Decimal
from django.conf import settings
from symbiarts_app.models import Obra


class Carrito(object):
    def __init__(self, request):
        self.session = request.session
        carrito = self.session.get(settings.CARRITO_SESSION_ID)
        if not carrito:
            carrito = self.session[settings.CARRITO_SESSION_ID] = {}
        self.carrito = carrito

    def agregar_obra(self, obra, cantidad=1, actualizar_cantidad=False):
        obra_id = str(obra.id)
        if obra_id not in self.carrito:
            self.carrito[obra_id] = {'cantidad': 0, 'precio': str(obra.precio)}
        if actualizar_cantidad:
            self.carrito[obra_id]['cantidad'] = cantidad
        else:
            self.carrito[obra_id]['cantidad'] += cantidad
        self.guardar()

    def guardar(self):
        self.session[settings.CARRITO_SESSION_ID] = self.carrito
        self.session.modified = True

    def eliminar_obra(self, obra):
        obra_id = str(obra.id)
        if obra_id in self.carrito:
            del self.carrito[obra_id]
            self.guardar()

    def __iter__(self):
        obra_ids = self.carrito.keys()
        obras = Obra.objects.filter(id__in=obra_ids)
        for obra in obras:
            self.carrito[str(obra.id)]['obra'] = obra

        for item in self.carrito.values():
            item['precio'] = Decimal(item['precio'])
            item['precio_total'] = item['precio'] * item['cantidad']
            yield item

    def __len__(self):
        return sum(item['cantidad'] for item in self.carrito.values())

    def obtener_precio_total(self):
        return sum(
            Decimal(item['precio']) * item['cantidad']
            for item in self.carrito.values()
            )

    def clear(self):
        del self.session[settings.CARRITO_SESSION_ID]
        self.session.modified = True

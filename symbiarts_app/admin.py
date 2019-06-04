from django.contrib import admin

from .models import Obra, ObraArchivo, Comentario

admin.site.register(Obra)
admin.site.register(ObraArchivo)
admin.site.register(Comentario)

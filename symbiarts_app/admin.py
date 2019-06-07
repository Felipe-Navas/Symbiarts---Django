from django.contrib import admin

from .models import Categoria, Comentario, Obra, ObraArchivo

admin.site.register(Categoria)
admin.site.register(Comentario)
admin.site.register(Obra)
admin.site.register(ObraArchivo)

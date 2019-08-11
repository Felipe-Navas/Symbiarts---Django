from django.urls import path

from . import views

app_name = 'symbiarts_app'
urlpatterns = [
    path('', views.lista_obras, name='lista_obras'),
    path('buscar/', views.buscar_obras, name='buscar_obras'),
    path('obra/<int:obra_id>/compra/', views.orquestar_compra_carrito,
         name='orquestar_compra_carrito'),
    path('obra/<int:obra_id>/compra/confirmar', views.grabar_compra,
         name='grabar_compra'),
    path('compra_exitosa/<int:nro_compra>',
         views.compra_exitosa, name='compra_exitosa'),
    path('carrito/comprar', views.comprar_carrito, name='comprar_carrito'),
    path('carrito/comprar/confirmar', views.grabar_compra_carrito,
         name='grabar_compra_carrito'),
    path('obra/<int:pk>/editar/', views.editar_obra, name='editar_obra'),
    path('obra/<int:pk>/', views.detalle_obra, name='detalle_obra'),
    path('obra/nueva', views.nueva_obra, name='nueva_obra'),
    path('obra/<int:pk>/pausar/', views.pausar_obra, name='pausar_obra'),
    path('obra/<int:pk>/reactivar/', views.reactivar_obra,
         name='reactivar_obra'),
    path('obra/<int:pk>/comentar/', views.nuevo_comentario,
         name='nuevo_comentario'),
    path('compras/', views.lista_compras, name='lista_compras'),
    path('compra/<int:compra_id>/', views.detalle_compra,
         name='detalle_compra'),
    path('ventas/', views.lista_ventas, name='lista_ventas'),
    path('venta/<int:venta_id>/', views.detalle_venta,
         name='detalle_venta'),
    path('comentario/<int:pk>/eliminar/', views.eliminar_comentario,
         name='eliminar_comentario')
]

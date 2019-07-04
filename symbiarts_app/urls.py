from django.urls import path

from . import views

app_name = 'symbiarts_app'
urlpatterns = [
    path('', views.lista_obras, name='lista_obras'),
    path('buscar/', views.buscar_obras, name='buscar_obras'),
    path('obra/<int:obra_id>/compra/', views.orquestar_compra_carrito,
         name='orquestar_compra_carrito'),
    path('obra/<int:pk>/editar/', views.editar_obra, name='editar_obra'),
    path('obra/<int:pk>/', views.detalle_obra, name='detalle_obra'),
    path('obra/nueva', views.nueva_obra, name='nueva_obra'),
    path('obra/<pk>/eliminar/', views.eliminar_obra, name='eliminar_obra'),
    path('obra/<pk>/comentar/', views.nuevo_comentario,
         name='nuevo_comentario'),
    path('comentario/<pk>/eliminar/', views.eliminar_comentario,
         name='eliminar_comentario')
]

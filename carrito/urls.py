from django.urls import path
from . import views

app_name = 'carrito'

urlpatterns = [
    path('', views.detalle_carrito, name='detalle_carrito'),
    path('add/<obra_id>/', views.agregar_obra_carrito, name='agregar_obra_carrito'),
    path('remove/<obra_id>/', views.eliminar_obra_carrito, name='eliminar_obra_carrito'),
]

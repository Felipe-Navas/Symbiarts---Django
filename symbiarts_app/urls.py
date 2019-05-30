from django.urls import path

from . import views

app_name = 'symbiarts_app'
urlpatterns = [
    path('', views.lista_obras, name='lista_obras'),
    path('obra/<int:pk>/', views.detalle_obra, name='detalle_obra'),
    path('obra/new', views.nueva_obra, name='nueva_obra'),
    path('obra/<int:pk>/edit/', views.editar_obra, name='editar_obra'),
    path('obra/<pk>/remove/', views.eliminar_obra, name='eliminar_obra'),
    # path('post/<pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    # path('comment/<pk>/approve/', views.comment_approve, name='comment_approve'),
    # path('comment/<pk>/remove/', views.comment_remove, name='comment_remove'),
]

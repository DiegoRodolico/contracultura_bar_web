from django.urls import path
from . import views

urlpatterns = [
    path('',views.base, name='base'),
    path('cliente',views.cliente, name = 'cliente'),
    path('agregar_cliente',views.agregar_cliente, name = 'agregar_cliente'),
    path('mesas',views.mesas, name = 'mesas'),
    path('mostrar_mesas',views.mostrar_mesas, name = 'mostrar_mesas'),
    path('pedido',views.pedido, name = 'pedido'),
    path('generar_pedido',views.generar_pedido, name = 'generar_pedido'),
    path('producto',views.producto, name = 'producto'),

]
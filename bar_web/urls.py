from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard, name='dashboard'),
    path('stock_critico',views.stock_critico, name = 'stock_critico'),
    path('reponer',views.reponer, name = 'reponer'),
    path('reponer_stock/<int:producto_id>',views.reponer_stock, name = 'reponer_stock'),
    path('cliente',views.cliente, name = 'cliente'),
    path('agregar_cliente',views.agregar_cliente, name = 'agregar_cliente'),
    path('editar_cliente/<int:cliente_id>',views.editar_cliente, name = 'editar_cliente'),
    path('eliminar_cliente/<int:cliente_id>',views.eliminar_cliente, name = 'eliminar_cliente'),
    path('mesas',views.mesas, name = 'mesas'),
    path('mostrar_mesas',views.mostrar_mesas, name = 'mostrar_mesas'),
    path('pedido',views.pedido, name = 'pedido'),
    path('iniciar_pedido',views.iniciar_pedido, name = 'iniciar_pedido'),
    path('ticket_pedido/<int:pedido_id>',views.ticket_pedido, name = 'ticket_pedido'),
    path('editar_detalle/<int:detalle_id>',views.editar_detalle, name = 'editar_detalle'),
    path('eliminar_detalle/<int:detalle_id>',views.eliminar_detalle, name = 'eliminar_detalle'),
    path('cerrar_pedido/<int:pedido_id>',views.cerrar_pedido, name = 'cerrar_pedido'),
    path('cancelar_pedido/<int:pedido_id>',views.cancelar_pedido, name = 'cancelar_pedido'),
    path('producto',views.producto, name = 'producto'),
]
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('',views.dashboard, name='dashboard'),
#     path('stock_critico',views.stock_critico, name = 'stock_critico'),
#     path('reponer',views.reponer, name = 'reponer'),
#     path('reponer_stock/<int:producto_id>',views.reponer_stock, name = 'reponer_stock'),
#     path('cliente',views.cliente, name = 'cliente'),
#     path('agregar_cliente',views.agregar_cliente, name = 'agregar_cliente'),
#     path('editar_cliente/<int:cliente_id>',views.editar_cliente, name = 'editar_cliente'),
#     path('eliminar_cliente/<int:cliente_id>',views.eliminar_cliente, name = 'eliminar_cliente'),
#     path('mesas',views.mesas, name = 'mesas'),
#     path('mostrar_mesas',views.mostrar_mesas, name = 'mostrar_mesas'),
#     path('pedido',views.pedido, name = 'pedido'),
#     path('iniciar_pedido',views.iniciar_pedido, name = 'iniciar_pedido'),
#     path('cerrar_pedido/<int:pedido_id>',views.cerrar_pedido, name = 'cerrar_pedido'),
#     path('cancelar_pedido/<int:pedido_id>',views.cancelar_pedido, name = 'cancelar_pedido'),
#     path('pedido/<int:pedido_id>/cancelar', views.cancelar_pedido, name='cancelar_pedido'),
#     path('pedido/<int:pedido_id>/entregar', views.entregar_pedido, name='entregar_pedido'),
#     path('ticket_pedido/<int:pedido_id>',views.ticket_pedido, name = 'ticket_pedido'),
#     path('editar_detalle/<int:detalle_id>',views.editar_detalle, name = 'editar_detalle'),
#     path('eliminar_detalle/<int:detalle_id>',views.eliminar_detalle, name = 'eliminar_detalle'),
#     path('cerrar_pedido/<int:pedido_id>',views.cerrar_pedido, name = 'cerrar_pedido'),
#     path('producto',views.producto, name = 'producto'),

# ]
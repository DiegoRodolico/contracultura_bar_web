from django.contrib import admin
from .models import Categorias, Clientes, DetallePedido, Mesas, Pedidos, Productos

admin.site.register(Clientes)
admin.site.register(Categorias)
admin.site.register(Productos)
admin.site.register(DetallePedido)
admin.site.register(Mesas)
admin.site.register(Pedidos)

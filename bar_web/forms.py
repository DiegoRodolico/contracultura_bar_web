from django import forms
from .models import Clientes, DetallePedido

class clienteForm (forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['nombre', 'telefono']

class pedidoForm (forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal']

    
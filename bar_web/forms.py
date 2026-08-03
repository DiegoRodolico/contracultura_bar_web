from django import forms
from .models import Clientes, DetallePedido, Pedidos, Mesas


class clienteForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['nombre', 'telefono']


class iniciarPedidoForm(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields = ['tipo', 'mesa', 'cliente']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mesa'].queryset = Mesas.objects.filter(estado='LIBRE')
        self.fields['mesa'].required = False
        self.fields['cliente'].required = False

class pedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad']

    def clean_cantidad(self):
        cantidad = self.cleaned_data['cantidad']
        if cantidad <= 0:
            raise forms.ValidationError('La cantidad debe ser mayor a 0.')
        return cantidad

class editarDetalleForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['cantidad']

    def clean_cantidad(self):
        cantidad = self.cleaned_data['cantidad']
        if cantidad <= 0:
            raise forms.ValidationError('La cantidad debe ser mayor a 0.')
        return cantidad  
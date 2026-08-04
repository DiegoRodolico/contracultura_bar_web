from django import forms
from .models import Clientes, DetallePedido, Pedidos, Mesas, Productos


class clienteForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['nombre', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Juan Pérez',
                'autofocus': True,
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 11 2345-6789',
            }),
        }
        labels = {
            'nombre': 'Nombre completo',
            'telefono': 'Teléfono',
        }

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if not nombre:
            raise forms.ValidationError('El nombre no puede estar vacío.')
        return nombre


class iniciarPedidoForm(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields = ['tipo', 'mesa', 'cliente']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mesa'].queryset = Mesas.objects.all()
        self.fields['mesa'].required = False
        self.fields['cliente'].required = False

    def clean_mesa(self):
        mesa = self.cleaned_data.get('mesa')
        tipo = self.cleaned_data.get('tipo')
        if tipo == 'MESA' and mesa is None:
            raise forms.ValidationError('Para un pedido de tipo MESA tenés que elegir una mesa.')
        if mesa and mesa.estado != 'LIBRE':
            raise forms.ValidationError(f'La mesa {mesa.numero} no está libre ({mesa.get_estado_display()}).')
        return mesa

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


class reponerStockForm(forms.Form):
    cantidad = forms.IntegerField(
        min_value=1,
        label='Cantidad a reponer',
        help_text='Se sumará al stock actual.',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'autofocus': True}),
    )
    nuevo_stock_minimo = forms.IntegerField(
        required=False,
        min_value=0,
        label='Nuevo stock mínimo (opcional)',
        help_text='Dejar vacío para no modificarlo.',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
    )

    def clean_cantidad(self):
        cantidad = self.cleaned_data['cantidad']
        if cantidad <= 0:
            raise forms.ValidationError('La cantidad debe ser mayor a 0.')
        return cantidad
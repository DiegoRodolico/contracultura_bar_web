# models.py preparado para SQLite - Django gestiona las tablas.
from django.db import models


class Cajas(models.Model):
    fecha_apertura = models.DateTimeField(blank=True, null=True)
    fecha_cierre = models.DateTimeField(blank=True, null=True)
    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    monto_final = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estado = models.CharField(max_length=7, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey('Clientes', models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return f"Caja #{self.id}"


class IconosCategoria(models.TextChoices):
    CERVEZAS_ARTESANALES = '🍺', 'Cerveza Artesanal'
    CERVEZAS_INDUSTRIALES = '🍻', 'Cerveza Industrial'
    TRAGOS = '🍸', 'Trago'
    BURGUERS = '🍔', 'Hamburguesa'
    PA_PICAR = '🍟', 'Entrada'
    PIZZAS = '🍕', 'Pizza'
    VINOS = '🍷', 'Vino'
    CAFE = '☕', 'Café'
    BEBIDA_FRIA = '🥤', 'Bebida Fria'
    COSAS_RICAS = '🥐', 'Cosas Ricas'
    ALMUERZOS = '🍞', 'Almuerzos'
    PROMOS = '💡', 'Promos'


class Categorias(models.Model):
    nombre = models.CharField(unique=True, max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    icono = models.CharField(max_length=5, choices=IconosCategoria, default=IconosCategoria.CERVEZAS_ARTESANALES)

    def __str__(self):
        return f"{self.nombre} {self.icono} "


class Clientes(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    puntos = models.IntegerField(blank=True, null=True, default=0)
    fecha_registro = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.nombre


class EstadoPedido(models.TextChoices):
    PENDIENTE = 'PENDIENTE'
    PREPARANDO = 'PREPARANDO'
    LISTO = 'LISTO'
    CANCELADO = 'CANCELADO'
    ENTREGADO = 'ENTREGADO'


class EstadoMesa(models.TextChoices):
    LIBRE = 'LIBRE'
    OCUPADA = 'OCUPADA'
    RESERVADA = 'RESERVADA'


class UbicacionMesa(models.TextChoices):
    INTERIOR = 'INTERIOR'
    AFUERA = 'AFUERA'
    BARRA = 'BARRA'
    EXTERIOR = 'EXTERIOR'
    SILLON = 'SILLON'


class Mesas(models.Model):
    numero = models.IntegerField(unique=True)
    capacidad = models.IntegerField(blank=True, null=True, default=4)
    ubicacion = models.CharField(max_length=20, choices=UbicacionMesa.choices, default=UbicacionMesa.INTERIOR)
    estado = models.CharField(max_length=20, choices=EstadoMesa.choices, default=EstadoMesa.LIBRE)

    def __str__(self):
        return f"Mesa N° {self.numero}"


class TipoPedido(models.TextChoices):
    MESA = 'MESA'
    BARRA = 'BARRA'
    PARA_LLEVAR = 'PARA LLEVAR'


class Pedidos(models.Model):
    mesa = models.ForeignKey(Mesas, models.DO_NOTHING, blank=True, null=True)
    cliente = models.ForeignKey(Clientes, models.DO_NOTHING, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=EstadoPedido.choices, default=EstadoPedido.PENDIENTE)
    tipo = models.CharField(max_length=11, choices=TipoPedido.choices, default=TipoPedido.MESA)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    observaciones = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_cierre = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Pedido #{self.id}"


class Productos(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categorias, models.CASCADE, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(blank=True, null=True, default=0)
    stock_minimo = models.IntegerField(blank=True, null=True, default=5)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.nombre


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedidos, models.CASCADE, blank=True, null=True)
    producto = models.ForeignKey(Productos, models.DO_NOTHING, blank=True, null=True)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=EstadoPedido.choices, default=EstadoPedido.PENDIENTE)


class MovimientosCaja(models.Model):
    caja = models.ForeignKey(Cajas, models.DO_NOTHING)
    tipo = models.CharField(max_length=8)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=200)
    pedido = models.ForeignKey(Pedidos, models.DO_NOTHING, blank=True, null=True)
    referencia = models.CharField(max_length=50, blank=True, null=True)
    fecha_movimiento = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class MovimientosInventario(models.Model):
    producto = models.ForeignKey(Productos, models.DO_NOTHING)
    tipo = models.CharField(max_length=7)
    cantidad = models.IntegerField()
    motivo = models.CharField(max_length=200, blank=True, null=True)
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    usuario_id = models.IntegerField(blank=True, null=True)
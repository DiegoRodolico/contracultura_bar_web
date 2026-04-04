# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Cajas(models.Model):
    fecha_apertura = models.DateTimeField(blank=True, null=True)
    fecha_cierre = models.DateTimeField(blank=True, null=True)
    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    monto_final = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estado = models.CharField(max_length=7, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey('Clientes', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cajas'

class IconosCategoria(models.TextChoices):
    CERVEZAS_ARTESANALES= '🍺', 'Cerveza Artesanal',
    CERVEZAS_INDUSTRIALES= '🍻', 'Cerveza Industrial'
    TRAGOS = '🍸', 'Trago',
    BURGUERS = '🍔', 'Hamburguesa',
    PA_PICAR = '🍟', 'Entrada',
    PIZZAS = '🍕', 'Pizza',
    VINOS = '🍷', 'Vino',
    CAFE = '☕', 'Café',
    BEBIDA_FRIA = '🥤', 'Bebida Fria',
    COSAS_RICAS = '🥐', 'Cosas Ricas',
    ALMUERZOS = '🍞', 'Almuerzos',
    PROMOS = '💡', 'Promos'

class Categorias(models.Model):
    nombre = models.CharField(unique=True, max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    icono = models.CharField(max_length=5, choices=IconosCategoria, default=IconosCategoria.CERVEZAS_ARTESANALES)

    class Meta:
        managed = False
        db_table = 'categorias'
    
    def __str__(self):
        return f"{self.nombre} {self.icono} "
        
        


class Clientes(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    puntos = models.IntegerField(blank=True, null=True)
    fecha_registro = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clientes'

    def __str__(self):
        return self.nombre

class EstadoPedido(models.TextChoices):
    PENDIENTE = 'PENDIENTE'
    PREPARANDO ='PREPARANDO'
    LISTO ='LISTO'
    CANCELADO = 'CANCELADO'
    ENTREGADO = 'ENTREGADO'

class DetallePedido(models.Model):
    pedido = models.ForeignKey('Pedidos', models.DO_NOTHING, blank=True, null=True)
    producto = models.ForeignKey('Productos', models.DO_NOTHING, blank=True, null=True)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=EstadoPedido.choices, default=EstadoPedido.PENDIENTE)

    class Meta:
        managed = False
        db_table = 'detalle_pedido'

class EstadoMesa (models.Choices):
    LIBRE = 'LIBRE'
    OCUPADA = 'OCUPADA'
    RESERVADA = 'RESERVADA'

class UbicacionMesa (models.Choices):
    INTERIOR = 'INTERIOR' 
    AFUERA = 'AFUERA'
    BARRA = 'BARRA'
    EXTERIOR = 'EXTERIOR'
    SILLON = 'SILLON'

class Mesas(models.Model):
    numero = models.IntegerField(unique=True)
    capacidad = models.IntegerField(blank=True, null=True)
    ubicacion = models.CharField(max_length=20, choices=UbicacionMesa.choices, default=UbicacionMesa.INTERIOR)
    estado = models.CharField(max_length=20, choices=EstadoMesa.choices, default=EstadoMesa.LIBRE)

    class Meta:
        managed = False
        db_table = 'mesas'
    
    def __str__(self):
        return f"Mesa N° {self.numero}"

class MovimientosCaja(models.Model):
    caja = models.ForeignKey(Cajas, models.DO_NOTHING)
    tipo = models.CharField(max_length=8)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=200)
    pedido = models.ForeignKey('Pedidos', models.DO_NOTHING, blank=True, null=True)
    referencia = models.CharField(max_length=50, blank=True, null=True)
    fecha_movimiento = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movimientos_caja'


class MovimientosInventario(models.Model):
    producto = models.ForeignKey('Productos', models.DO_NOTHING)
    tipo = models.CharField(max_length=7)
    cantidad = models.IntegerField()
    motivo = models.CharField(max_length=200, blank=True, null=True)
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(blank=True, null=True)
    usuario_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movimientos_inventario'

class TipoPedido (models.Choices):
    MESA = 'MESA' 
    BARRA = 'BARRA' 
    PARA_LLEVAR = 'PARA LLEVAR'

class Pedidos(models.Model):
    mesa = models.ForeignKey(Mesas, models.DO_NOTHING, blank=True, null=True)
    cliente = models.ForeignKey(Clientes, models.DO_NOTHING, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=EstadoPedido.choices, default=EstadoPedido.PENDIENTE)
    tipo = models.CharField(max_length=11, choices=TipoPedido.choices, default=TipoPedido.MESA)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_cierre = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pedidos'
    
    def __str__(self):
        return f"Pedido #{self.id}"


class Productos(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categorias, models.CASCADE, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(blank=True, null=True)
    stock_minimo = models.IntegerField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.IntegerField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'productos'

    def __str__(self):
        return self.nombre

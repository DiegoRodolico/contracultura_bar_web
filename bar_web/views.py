from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from .models import Clientes, Productos, Mesas, Pedidos, Categorias, DetallePedido
from .forms import clienteForm, pedidoForm, iniciarPedidoForm, editarDetalleForm


def recalcular_total(pedido):
    total = sum(
        (d.subtotal or 0) for d in pedido.detallepedido_set.all()
    )
    pedido.total = total
    pedido.save()


def base(request):
    return render(request, 'base.html')


def cliente(request):
    cliente = Clientes.objects.all()
    return render(request, 'cliente.html', {'cliente': cliente})


def agregar_cliente(request):
    formulario_cliente = clienteForm(request.POST or None, request.FILES or None)
    if formulario_cliente.is_valid():
        formulario_cliente.save()
        return redirect('cliente')
    return render(request, 'agregar_cliente.html', {'formulario_cliente': formulario_cliente})


def mesas(request):
    mesas = Mesas.objects.all()
    mesas_libres = mesas.filter(estado='LIBRE').count()
    return render(request, 'mesas.html', {
        'mesas': mesas,
        'mesas_libres': mesas_libres
    })


def mostrar_mesas(request):
    mesas = Mesas.objects.all()
    mesas_libres = mesas.filter(estado='LIBRE').count()
    return render(request, 'mostrar_mesas.html', {
        'mesas': mesas,
        'mesas_libres': mesas_libres,
    })


def pedido(request):
    pedidos = Pedidos.objects.all()
    return render(request, 'pedido.html', {'pedidos': pedidos})


def iniciar_pedido(request):
    formulario_inicial = iniciarPedidoForm(request.POST or None)
    if formulario_inicial.is_valid():
        pedido_nuevo = formulario_inicial.save()

        if pedido_nuevo.mesa:
            pedido_nuevo.mesa.estado = 'OCUPADA'
            pedido_nuevo.mesa.save()

        return redirect('ticket_pedido', pedido_id=pedido_nuevo.id)
    return render(request, 'iniciar_pedido.html', {'formulario_inicial': formulario_inicial})


def ticket_pedido(request, pedido_id):
    pedido_actual = get_object_or_404(Pedidos, id=pedido_id)
    formulario_pedido = pedidoForm(request.POST or None)
    error_stock = None

    if request.method == 'POST' and formulario_pedido.is_valid():
        detalle = formulario_pedido.save(commit=False)
        producto = detalle.producto
        if producto.stock < detalle.cantidad :
            error_stock = f"Stock insuficiente de {producto.nombre} (disponible: {producto.stock})"
        else:
            producto.stock -= detalle.cantidad
            producto.save()
            detalle.pedido = pedido_actual
            detalle.precio_unitario = detalle.producto.precio
            detalle.subtotal = detalle.precio_unitario * detalle.cantidad
            detalle.save()

            recalcular_total(pedido_actual)
            return redirect('ticket_pedido', pedido_id=pedido_actual.id)

    detalles = pedido_actual.detallepedido_set.all()
    return render(request, 'ticket_pedido.html', {
        'pedido': pedido_actual,
        'detalles': detalles,
        'formulario_pedido': formulario_pedido,
        'error_stock': error_stock,
    })


def editar_detalle(request, detalle_id):
    detalle = get_object_or_404(DetallePedido, id=detalle_id)
    formulario_editar = editarDetalleForm(request.POST or None, instance=detalle)
    cantidad_anterior = detalle.cantidad

    if formulario_editar.is_valid():
        detalle_editado = formulario_editar.save(commit=False)
        cantidad_nueva = detalle_editado.cantidad
        diferencia = cantidad_nueva - cantidad_anterior
        producto = detalle_editado.producto
        producto.stock -= diferencia
        producto.save()
        detalle_editado.subtotal = detalle_editado.precio_unitario * detalle_editado.cantidad
        detalle_editado.save()

        recalcular_total(detalle.pedido)
        return redirect('ticket_pedido', pedido_id=detalle.pedido.id)

    return render(request, 'editar_detalle.html', {
        'formulario_editar': formulario_editar,
        'detalle': detalle,
    })


def eliminar_detalle(request, detalle_id):
    detalle = get_object_or_404(DetallePedido, id=detalle_id)
    pedido_id = detalle.pedido.id
    producto = detalle.producto
    producto.stock += detalle.cantidad
    producto.save()

    detalle.delete()

    recalcular_total(get_object_or_404(Pedidos, id=pedido_id))
    return redirect('ticket_pedido', pedido_id=pedido_id)


def cerrar_pedido(request, pedido_id):
    pedido_actual = get_object_or_404(Pedidos, id=pedido_id)
    pedido_actual.fecha_cierre = timezone.now()
    pedido_actual.estado = 'ENTREGADO'
    pedido_actual.save()

    if pedido_actual.mesa:
        pedido_actual.mesa.estado = 'LIBRE'
        pedido_actual.mesa.save()

    return redirect('pedido')


def producto(request):
    producto = Productos.objects.all()
    return render(request, 'producto.html', {'producto': producto})
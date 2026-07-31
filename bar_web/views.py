from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Clientes, Productos, Mesas, Pedidos, Categorias, DetallePedido
from .forms import clienteForm, pedidoForm


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


def generar_pedido(request):
    formulario_pedido = pedidoForm(request.POST or None, request.FILES or None)
    if formulario_pedido.is_valid():
        formulario_pedido.save()
        return redirect('pedido')
    return render(request, 'generar_pedido.html', {'formulario_pedido': formulario_pedido})


def producto(request):
    producto = Productos.objects.all()
    return render(request, 'producto.html', {'producto': producto})
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Sum, F, Q, Case, When, Value, IntegerField, Prefetch
from django.contrib import messages
from datetime import timedelta
from .models import Clientes, Productos, Mesas, Pedidos, Categorias, DetallePedido
from .forms import clienteForm, pedidoForm, iniciarPedidoForm, editarDetalleForm, reponerStockForm


NIVEL_AGOTADO = 0
NIVEL_CRITICO = 1
NIVEL_BAJO = 2

NIVEL_LABELS = {
    NIVEL_AGOTADO: ('Agotado', 'danger'),
    NIVEL_CRITICO: ('Crítico', 'warning'),
    NIVEL_BAJO: ('Bajo', 'info'),
}


def nivel_stock(stock, stock_minimo):
    if stock is None or stock <= 0:
        return NIVEL_AGOTADO
    if stock_minimo and stock <= stock_minimo / 2:
        return NIVEL_CRITICO
    return NIVEL_BAJO


def productos_con_stock_bajo(solo_activos=True):
    qs = Productos.objects.all()
    if solo_activos:
        qs = qs.filter(activo=True)
    qs = qs.annotate(
        diferencia=F('stock_minimo') - F('stock'),
    ).filter(
        stock__lte=F('stock_minimo')
    ).order_by('diferencia', 'nombre')

    for p in qs:
        p.nivel = nivel_stock(p.stock, p.stock_minimo)
        p.nivel_label, p.nivel_color = NIVEL_LABELS[p.nivel]
        try:
            p.margen = (p.precio or 0) - (p.costo or 0)
        except TypeError:
            p.margen = 0
    return qs


def recalcular_total(pedido):
    total = sum(
        (d.subtotal or 0) for d in pedido.detallepedido_set.all()
    )
    pedido.total = total
    pedido.save()


def dashboard(request):
    hoy = timezone.localdate()
    inicio_hoy = timezone.make_aware(timezone.datetime.combine(hoy, timezone.datetime.min.time()))

    pedidos_hoy = Pedidos.objects.filter(fecha_creacion__gte=inicio_hoy)
    pedidos_abiertos = pedidos_hoy.exclude(estado__in=['ENTREGADO', 'CANCELADO'])

    total_facturado_hoy = pedidos_hoy.filter(estado='ENTREGADO').aggregate(
        s=Sum('total')
    )['s'] or 0

    stock_critico_qs = productos_con_stock_bajo()
    stock_critico_count = stock_critico_qs.count()
    stock_critico_top = list(stock_critico_qs[:5])

    agotados_count = sum(1 for p in stock_critico_qs if p.nivel == NIVEL_AGOTADO)
    criticos_count = sum(1 for p in stock_critico_qs if p.nivel == NIVEL_CRITICO)
    bajos_count = sum(1 for p in stock_critico_qs if p.nivel == NIVEL_BAJO)

    mesas_ocupadas = Mesas.objects.filter(estado='OCUPADA')
    mesas_libres = Mesas.objects.filter(estado='LIBRE').count()

    ultimos_pedidos = Pedidos.objects.all().order_by('-fecha_creacion')[:10]

    context = {
        'pedidos_abiertos_count': pedidos_abiertos.count(),
        'total_facturado_hoy': total_facturado_hoy,
        'stock_critico_count': stock_critico_count,
        'stock_agotados_count': agotados_count,
        'stock_criticos_count': criticos_count,
        'stock_bajos_count': bajos_count,
        'mesas_ocupadas_count': mesas_ocupadas.count(),
        'mesas_libres_count': mesas_libres,
        'stock_critico': stock_critico_top,
        'ultimos_pedidos': ultimos_pedidos,
    }
    return render(request, 'dashboard.html', context)


def stock_critico(request):
    productos = productos_con_stock_bajo()
    return render(request, 'stock_critico.html', {
        'productos': productos,
        'total_productos': productos.count(),
    })


MODO_TODOS = 'todos'
MODO_CRITICOS = 'criticos'


def reponer(request):
    modo = request.GET.get('modo', MODO_CRITICOS)
    if modo not in (MODO_CRITICOS, MODO_TODOS):
        modo = MODO_CRITICOS

    q = (request.GET.get('q') or '').strip()
    categoria_id = request.GET.get('categoria') or ''

    if modo == MODO_CRITICOS:
        qs = productos_con_stock_bajo()
    else:
        qs = Productos.objects.filter(activo=True).order_by('nombre')
        for p in qs:
            p.nivel = nivel_stock(p.stock, p.stock_minimo)
            p.nivel_label, p.nivel_color = NIVEL_LABELS[p.nivel]
            try:
                p.margen = (p.precio or 0) - (p.costo or 0)
            except TypeError:
                p.margen = 0
            p.diferencia = (p.stock_minimo or 0) - (p.stock or 0)

    if q:
        qs = [p for p in qs if q.lower() in p.nombre.lower()]

    categorias_list = Categorias.objects.all().order_by('nombre')
    if categoria_id:
        try:
            qs = [p for p in qs if p.categoria_id == int(categoria_id)]
        except (ValueError, TypeError):
            categoria_id = ''

    total_productos = len(qs) if isinstance(qs, list) else qs.count()

    return render(request, 'reponer.html', {
        'productos': qs,
        'total_productos': total_productos,
        'modo': modo,
        'q': q,
        'categoria_id': str(categoria_id),
        'categorias': categorias_list,
    })


def reponer_stock(request, producto_id):
    producto = get_object_or_404(Productos, id=producto_id)
    stock_anterior = producto.stock or 0
    next_url = request.GET.get('next') or request.POST.get('next') or ''

    if request.method == 'POST':
        form = reponerStockForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']
            nuevo_minimo = form.cleaned_data.get('nuevo_stock_minimo')

            producto.stock = stock_anterior + cantidad
            if nuevo_minimo is not None:
                producto.stock_minimo = nuevo_minimo
            producto.save()

            messages.success(
                request,
                f'Stock de "{producto.nombre}" actualizado: {stock_anterior} → {producto.stock}.'
            )
            if next_url:
                return redirect(next_url)
            return redirect('stock_critico')
    else:
        form = reponerStockForm(initial={'nuevo_stock_minimo': producto.stock_minimo})

    nivel = nivel_stock(producto.stock, producto.stock_minimo)
    nivel_label, nivel_color = NIVEL_LABELS[nivel]

    return render(request, 'reponer_stock.html', {
        'producto': producto,
        'stock_anterior': stock_anterior,
        'form': form,
        'nivel': nivel,
        'nivel_label': nivel_label,
        'nivel_color': nivel_color,
        'next_url': next_url,
    })


def cliente(request):
    cliente = Clientes.objects.all()
    return render(request, 'cliente.html', {'cliente': cliente})


def agregar_cliente(request):
    formulario_cliente = clienteForm(request.POST or None, request.FILES or None)
    if formulario_cliente.is_valid():
        formulario_cliente.save()
        return redirect('cliente')
    return render(request, 'agregar_cliente.html', {'formulario_cliente': formulario_cliente})

def editar_cliente(request, cliente_id):
    cliente_actual = get_object_or_404(Clientes, id=cliente_id)
    formulario_cliente = clienteForm(request.POST or None, instance=cliente_actual)
    if formulario_cliente.is_valid():
        formulario_cliente.save()
        messages.success(request, f'Cliente "{cliente_actual.nombre}" actualizado.')
        return redirect('cliente')
    return render(request, 'editar_cliente.html', {
        'formulario_cliente': formulario_cliente,
        'cliente': cliente_actual,
    })

def eliminar_cliente(request, cliente_id):
    cliente_actual = get_object_or_404(Clientes, id=cliente_id)
    nombre = cliente_actual.nombre
    cliente_actual.delete()
    messages.success(request, f'Cliente "{nombre}" eliminado.')
    return redirect('cliente')


def mesas(request):
    mesas, mesas_libres, mesas_ocupadas, mesas_reservadas = _mesas_para_grid()
    return render(request, 'mesas.html', {
        'mesas': mesas,
        'mesas_libres': mesas_libres,
        'mesas_ocupadas': mesas_ocupadas,
        'mesas_reservadas': mesas_reservadas,
    })


def mostrar_mesas(request):
    mesas, mesas_libres, mesas_ocupadas, mesas_reservadas = _mesas_para_grid()
    return render(request, 'mostrar_mesas.html', {
        'mesas': mesas,
        'mesas_libres': mesas_libres,
        'mesas_ocupadas': mesas_ocupadas,
        'mesas_reservadas': mesas_reservadas,
    })


def pedido(request):
    pedidos_activos = Pedidos.objects.filter(estado='ACTIVO').order_by('-fecha_creacion')
    pedidos_historial = Pedidos.objects.exclude(estado='ACTIVO').order_by('-fecha_cierre', '-fecha_creacion')
    vista = request.GET.get('vista', 'activos')
    if vista not in ('activos', 'historial'):
        vista = 'activos'

    q = (request.GET.get('q') or '').strip()
    estado = (request.GET.get('estado') or '').strip()

    activos_estados = ['PENDIENTE', 'PREPARANDO', 'LISTO']
    cerrados_estados = ['ENTREGADO', 'CANCELADO']

    if vista == 'activos':
        qs = Pedidos.objects.filter(estado__in=activos_estados)
    else:
        qs = Pedidos.objects.filter(estado__in=cerrados_estados)

    if estado and estado in (activos_estados + cerrados_estados):
        qs = qs.filter(estado=estado)

    if q:
        if q.isdigit():
            qs = qs.filter(id=int(q))
        else:
            qs = qs.filter(
                Q(cliente__nombre__icontains=q) |
                Q(mesa__numero__icontains=q)
            )

    qs = qs.select_related('mesa', 'cliente').order_by('-fecha_creacion')

    activos_count = Pedidos.objects.filter(estado__in=activos_estados).count()
    cerrados_count = Pedidos.objects.filter(estado__in=cerrados_estados).count()

    page_obj = None
    paginated = False
    if vista == 'historial':
        from django.core.paginator import Paginator
        paginator = Paginator(qs, 20)
        page_number = request.GET.get('page') or 1
        try:
            page_obj = paginator.page(int(page_number))
        except Exception:
            page_obj = paginator.page(1)
        pedidos = page_obj.object_list
        paginated = True
    else:
        pedidos = list(qs[:100])

    return render(request, 'pedido.html', {
        'pedidos': pedidos,
        'vista': vista,
        'q': q,
        'estado': estado,
        'estados_activos': activos_estados,
        'estados_cerrados': cerrados_estados,
        'activos_count': activos_count,
        'cerrados_count': cerrados_count,
        'page_obj': page_obj,
        'paginated': paginated,
        'pedidos_activos': pedidos_activos,
        'pedidos_historial': pedidos_historial,
    })


def _mesas_para_grid():
    mesas_qs = Mesas.objects.all().order_by('numero')
    mesas = []
    mesas_libres = 0
    mesas_ocupadas = 0
    mesas_reservadas = 0

    for mesa in mesas_qs:
        if mesa.estado == 'OCUPADA':
            mesas_ocupadas += 1
        elif mesa.estado == 'RESERVADA':
            mesas_reservadas += 1
        else:
            mesas_libres += 1

        mesas.append({
            'obj': mesa,
            'id': mesa.id,
            'numero': mesa.numero,
            'estado': mesa.estado,
            'ubicacion': mesa.get_ubicacion_display(),
            'capacidad': mesa.capacidad,
        })

    return mesas, mesas_libres, mesas_ocupadas, mesas_reservadas


def iniciar_pedido(request):
    formulario_inicial = iniciarPedidoForm(request.POST or None)
    if request.method == 'POST' and formulario_inicial.is_valid():
        pedido_nuevo = formulario_inicial.save()

        if pedido_nuevo.mesa:
            pedido_nuevo.mesa.estado = 'OCUPADA'
            pedido_nuevo.mesa.save()

        return redirect('ticket_pedido', pedido_id=pedido_nuevo.id)

    mesas, mesas_libres, mesas_ocupadas, mesas_reservadas = _mesas_para_grid()

    return render(request, 'iniciar_pedido.html', {
        'formulario_inicial': formulario_inicial,
        'mesas': mesas,
        'mesas_libres': mesas_libres,
        'mesas_ocupadas': mesas_ocupadas,
        'mesas_reservadas': mesas_reservadas,
    })


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

def cancelar_pedido(request, pedido_id):
    pedido_actual = get_object_or_404(Pedidos, id=pedido_id)

    for detalle in pedido_actual.detallepedido_set.all():
        producto = detalle.producto
        if producto:
            producto.stock = (producto.stock or 0) + detalle.cantidad
            producto.save()

    pedido_actual.fecha_cierre = timezone.now()
    pedido_actual.estado = 'CANCELADO'
    pedido_actual.save()

    if pedido_actual.mesa:
        pedido_actual.mesa.estado = 'LIBRE'
        pedido_actual.mesa.save()

    messages.info(request, f'Pedido #{pedido_actual.id} cancelado y stock repuesto.')
    return redirect('pedido')

def producto(request):
    categorias = Categorias.objects.prefetch_related(
        Prefetch(
            'productos_set',
            queryset=Productos.objects.filter(activo=True).order_by('nombre')
        )
    ).order_by('nombre')

    # Productos sin categoría asignada (categoria puede ser null)
    productos_sin_categoria = Productos.objects.filter(
        categoria__isnull=True, activo=True
    ).order_by('nombre')

    return render(request, 'producto.html', {
        'categorias': categorias,
        'productos_sin_categoria': productos_sin_categoria,
    })


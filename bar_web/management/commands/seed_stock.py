from django.core.management.base import BaseCommand
from django.db import transaction
from bar_web.models import Categorias, Productos, IconosCategoria


CATEGORIAS = [
    ('Cervezas', IconosCategoria.CERVEZAS_ARTESANALES),
    ('Tragos', IconosCategoria.TRAGOS),
    ('Hamburguesas', IconosCategoria.BURGUERS),
    ('Pizzas', IconosCategoria.PIZZAS),
    ('Bebidas', IconosCategoria.BEBIDA_FRIA),
]


PRODUCTOS = [
    # (nombre, categoria, precio, costo, stock, stock_minimo, activo)
    # --- AGOTADOS (stock = 0) ---
    ('IPA Artesanal', 'Cervezas', 1800, 700, 0, 12, True),
    ('Fernet Coca', 'Tragos', 2200, 800, 0, 10, True),

    # --- CRÍTICOS (stock <= 50% del mínimo) ---
    ('Stout Ahumada', 'Cervezas', 2000, 850, 3, 12, True),       # mín 12, 50% = 6, stock 3 → crítico
    ('Gin Tonic', 'Tragos', 2800, 1000, 2, 10, True),            # mín 10, 50% = 5, stock 2 → crítico
    ('Burger Doble', 'Hamburguesas', 4500, 1800, 4, 10, True),   # mín 10, 50% = 5, stock 4 → crítico

    # --- BAJOS (entre 50% del mínimo y el mínimo) ---
    ('Lager', 'Cervezas', 1500, 600, 7, 10, True),               # mín 10, 50% = 5, stock 7 → bajo
    ('Mojito', 'Tragos', 2500, 900, 6, 10, True),                # mín 10, 50% = 5, stock 6 → bajo
    ('Muzza', 'Pizzas', 5500, 2000, 4, 6, True),                 # mín 6,  50% = 3, stock 4 → bajo
    ('Coca-Cola 1.5L', 'Bebidas', 1500, 700, 8, 12, True),       # mín 12, 50% = 6, stock 8 → bajo

    # --- NORMALES (por encima del mínimo, no deberían aparecer) ---
    ('Patagonia Amber', 'Cervezas', 1800, 700, 24, 10, True),
    ('Daikiri', 'Tragos', 2600, 950, 15, 8, True),
    ('Burger Simple', 'Hamburguesas', 3800, 1500, 20, 10, True),
    ('Pizza Napolitana', 'Pizzas', 6000, 2200, 12, 6, True),
    ('Agua 500ml', 'Bebidas', 800, 300, 50, 20, True),
    ('Cerveza Inactiva', 'Cervezas', 1500, 600, 0, 10, False),   # inactivo, debería NO aparecer
]


class Command(BaseCommand):
    help = 'Carga productos y categorías de prueba para verificar el stock crítico'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Borra los productos y categorías previos antes de cargar',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['reset']:
            borrados_prod = Productos.objects.filter(nombre__in=[p[0] for p in PRODUCTOS]).delete()
            borrados_cat = Categorias.objects.filter(nombre__in=[c[0] for c in CATEGORIAS]).delete()
            self.stdout.write(self.style.WARNING(
                f'Reset: {borrados_prod[0]} productos y {borrados_cat[0]} categorías borradas.'
            ))

        cats = {}
        for nombre, icono in CATEGORIAS:
            cat, created = Categorias.objects.get_or_create(
                nombre=nombre,
                defaults={'icono': icono, 'descripcion': f'Categoría {nombre}'},
            )
            cats[nombre] = cat
            accion = 'creada' if created else 'ya existía'
            self.stdout.write(f'  categoría: {nombre} ({accion})')

        creados = 0
        actualizados = 0
        for nombre, cat_nombre, precio, costo, stock, stock_minimo, activo in PRODUCTOS:
            obj, created = Productos.objects.update_or_create(
                nombre=nombre,
                defaults={
                    'categoria': cats[cat_nombre],
                    'precio': precio,
                    'costo': costo,
                    'stock': stock,
                    'stock_minimo': stock_minimo,
                    'activo': activo,
                },
            )
            if created:
                creados += 1
            else:
                actualizados += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nListo: {creados} productos creados, {actualizados} actualizados.'
        ))

        self.stdout.write('\nResumen esperado:')
        self.stdout.write('  AGOTADOS (2):  IPA Artesanal, Fernet Coca')
        self.stdout.write('  CRÍTICOS (3):  Stout Ahumada, Gin Tonic, Burger Doble')
        self.stdout.write('  BAJOS (4):     Lager, Mojito, Muzza, Coca-Cola 1.5L')
        self.stdout.write('  NORMALES (5):  no aparecen en el listado')
        self.stdout.write('  INACTIVO (1):  Cerveza Inactiva (no aparece por estar inactivo)')
        self.stdout.write(self.style.SUCCESS(
            '\nIr a http://127.0.0.1:8000/stock_critico para ver el detalle.'
        ))

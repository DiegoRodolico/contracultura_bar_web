# 🍺 Contracultura Bar - Sistema de Gestión

🍺 Contracultura Bar - Sistema de Gestión

Aplicación web desarrollada con Django para la gestión integral de un bar. Permite administrar productos, categorías, clientes, mesas y pedidos desde una interfaz simple y funcional.

🚀 Funcionalidades
📦 Gestión de productos (alta, baja, modificación)
🗂️ Gestión de categorías
👤 Gestión de clientes
🍽️ Administración de mesas (ocupación y disponibilidad)
🧾 Creación de pedidos
📊 Base para dashboard de control
🔗 Relación entre productos y categorías
⚡ Interfaz con Bootstrap
🛠️ Tecnologías utilizadas
Python 3
Django
SQLite 
Bootstrap 5
HTML / CSS / JS

ℹ️ Nota: el proyecto originalmente usaba MySQL con tablas creadas por fuera de Django. Se migró a SQLite para simplificar el desarrollo: ahora Django gestiona la base completa a través de sus migraciones, sin necesidad de instalar ni configurar un servidor de base de datos aparte.

⚙️ Instalación (Linux)
* Clonar el repositorio:
```bash
git clone https://github.com/DiegoRodolico/contracultura_bar_web.git
cd contracultura_bar_web
```
* Crear y activar el entorno virtual:
```bash
python3 -m venv venv
source venv/bin/activate
```
* Instalar dependencias:
```bash
pip install django
```
* Generar y aplicar las migraciones :
```bash
python manage.py makemigrations bar_web
python manage.py migrate
```
* Crear superusuario (para poder entrar a /admin y cargar datos):
```bash
python manage.py createsuperuser
```
* Levantar el servidor:
```bash
python manage.py runserver
```
* Abrir en el navegador:
  - App: http://127.0.0.1:8000/
  - Admin: http://127.0.0.1:8000/admin/
📋 Estado actual del proyecto
✅ Base de datos SQLite funcionando, esquema migrado.
⚠️ La base se crea vacía: no trae categorías, productos ni mesas de ejemplo. Para probar la app hay que cargar datos manualmente desde /admin (Categorías, Productos, Mesas) o armando un fixture/script de carga inicial.
🔜 Pendiente: cargar datos de prueba, revisar formularios de cliente y pedido (les falta manejo de errores/validación visual), y seguir sumando funcionalidades de caja e inventario (los modelos Cajas, MovimientosCaja y MovimientosInventario ya están definidos pero sin vistas ni templates todavía).

👨‍💻 Autor

Diego Rodolico GitHub: https://github.com/DiegoRodolico

📄 Licencia

Uso libre para aprendizaje y desarrollo personal.

# 🍺 Contracultura Bar - Sistema de Gestión

Aplicación web desarrollada con Django para la gestión integral de un bar.  
Permite administrar productos, categorías, clientes, mesas y pedidos desde una interfaz simple y funcional.

---

## 🚀 Funcionalidades

- 📦 Gestión de productos (alta, baja, modificación)
- 🗂️ Gestión de categorías
- 👤 Gestión de clientes
- 🍽️ Administración de mesas (ocupación y disponibilidad)
- 🧾 Creación de pedidos
- 📊 Base para dashboard de control
- 🔗 Relación entre productos y categorías
- ⚡ Interfaz con Bootstrap

---

## 🛠️ Tecnologías utilizadas

- Python 3
- Django
- MySQL
- Bootstrap 5
- HTML / CSS / JS

---

## ⚙️ Instalación

1. Clonar el repositorio:

git clone https://github.com/DiegoRodolico/contracultura_bar_web.git
cd contracultura_bar_web

2. Crear entorno virtual:
python -m venv venv
source venv/bin/activate  # Linux
venv\Scripts\activate     # Windows

3. Instalar dependencias:
pip install -r requirements.txt

4. Configurar base de datos en settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'contracultura_bar',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

5. Ejecutar migraciones:
python manage.py migrate

6. Crear superusuario:
python manage.py createsuperuser

7. Levantar servidor:
python manage.py runserver

---

##  👨‍💻 Autor
Diego Rodolico
GitHub: https://github.com/DiegoRodolico

---

##  📄 Licencia
Uso libre para aprendizaje y desarrollo personal.

# MarketChile

Sistema web de gestión interna para **MarketChile**, una multitienda ficticia desarrollada con Django. La aplicación permite administrar usuarios y mantener el registro del equipo de trabajo de la empresa.

## Funcionalidades

- Registro, inicio y cierre de sesión; el dashboard y las operaciones de cuenta requieren autenticación.
- Dashboard de MarketChile con métricas calculadas desde la base de datos: empleados totales, activos e inactivos, departamentos y cargos.
- Listado de cargos disponibles en el dashboard, mostrando el departamento asociado y un estado vacío cuando no hay cargos registrados.
- Gestión de empleados: creación, listado, detalle, edición y eliminación con confirmación.
- Formularios de empleado con selección de cargo filtrada por departamento.
- Modelos relacionados de departamentos, cargos y empleados; se restringe eliminar departamentos o cargos que estén en uso.
- Edición del perfil y eliminación de la cuenta autenticada.
- Interfaz del dashboard adaptable a escritorio y dispositivos móviles.

## Permisos de gestión

- Los usuarios autenticados pueden consultar y filtrar el listado y ver el detalle de los empleados.
- Solo las cuentas administradoras (`is_staff`) pueden crear, editar o eliminar empleados. La restricción también se valida en las vistas, por lo que ocultar los botones no es la única protección.
- Para habilitar a un administrador, un superusuario debe marcar **Acceso al sitio de administración** en la cuenta desde `/admin/`. El registro público no permite activar este privilegio.

## Mejoras implementadas

- Se incorporaron en el dashboard las métricas de operación conectadas a los datos reales.
- Se muestra el catálogo de cargos con su departamento para consultar las opciones disponibles sin salir del dashboard.
- Se organizaron las operaciones frecuentes del equipo y accesos al perfil en el centro de operaciones.
- Se añadieron páginas para consultar el detalle del empleado y confirmar su eliminación.
- El formulario de empleados limita los cargos disponibles según el departamento seleccionado.
- Se mejoró la presentación responsive del dashboard y de las pantallas del módulo de personal con Bootstrap.

## Tecnologías

- Python
- Django 6.1.1
- SQLite
- Bootstrap 5.3.8
- HTML y CSS

## Estructura principal

```text
sistema_usuarios/
├── manage.py
├── db.sqlite3
├── proyecto/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── usuarios/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── templates/usuarios/
└── personal/
    ├── forms.py
    ├── models.py
    ├── urls.py
    ├── views.py
    └── templates/personal/
```

## Requisitos

- Python 3.10 o superior.
- `pip`.
- Windows, macOS o Linux.

## Instalación

1. Clona o descarga el proyecto.
2. Abre una terminal dentro de la carpeta `sistema_usuarios`.
3. Crea un entorno virtual:

```bash
python -m venv venv
```

4. Activa el entorno virtual.

En Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

En Windows CMD:

```cmd
venv\Scripts\activate
```

En macOS o Linux:

```bash
source venv/bin/activate
```

5. Instala Django:

```bash
pip install django
```

6. Ejecuta las migraciones:

```bash
python manage.py migrate
```

## Ejecutar el proyecto

Inicia el servidor de desarrollo con:

```bash
python manage.py runserver
```

Luego abre en el navegador:

```text
http://127.0.0.1:8000/
```

## Rutas principales

| Ruta | Descripción |
|---|---|
| `/` | Dashboard de MarketChile |
| `/login/` | Inicio de sesión |
| `/registro/` | Registro de usuarios |
| `/bienvenida/` | Dashboard autenticado |
| `/personal/` | Módulo de gestión de empleados |
| `/personal/inicio/` | Inicio del módulo de personal |
| `/editar-perfil/` | Edición del perfil |
| `/eliminar-cuenta/` | Eliminación de cuenta |
| `/logout/` | Cierre de sesión |

## Modelos de personal

- **Departamento:** representa las áreas de la empresa.
- **Cargo:** representa los cargos disponibles.
- **Empleado:** almacena RUT, nombre, apellido, correo, teléfono, fecha de ingreso, estado, cargo y departamento.

Los estados disponibles para un empleado son:

- `Activo`
- `Inactivo`

## Comandos útiles

Comprobar la configuración del proyecto:

```bash
python manage.py check
```

Crear nuevas migraciones después de modificar modelos:

```bash
python manage.py makemigrations
python manage.py migrate
```

Crear un usuario administrador:

```bash
python manage.py createsuperuser
```

Ejecutar las pruebas:

```bash
python manage.py test
```

## Administración

El panel administrativo de Django está disponible en:

```text
http://127.0.0.1:8000/admin/
```

Para acceder, primero crea un superusuario con `python manage.py createsuperuser`.

## Nota para producción

El proyecto está configurado para desarrollo. Antes de publicarlo, se deben cambiar la `SECRET_KEY`, desactivar `DEBUG`, configurar `ALLOWED_HOSTS`, utilizar variables de entorno y aplicar las recomendaciones de seguridad de Django.

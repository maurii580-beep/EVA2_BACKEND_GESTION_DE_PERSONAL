from django.urls import path
from . import views


urlpatterns = [
    # Ruta de inicio del módulo personal.
    path('inicio/', views.inicio, name='inicio'),

    # Ruta principal del módulo: /personal/
    path('', views.lista_empleados, name='lista_empleados'),

    # Ruta para crear: /personal/crear/
    path('crear/', views.crear_empleado, name='crear_empleado'),
    
    # Rutas que reciben el ID del empleado para ver detalle, editar o eliminar
    path('detalle/<int:empleado_id>/', views.detalle_empleado, name='detalle_empleado'),
    path('editar/<int:empleado_id>/', views.editar_empleado, name='editar_empleado'),
    path('eliminar/<int:empleado_id>/', views.eliminar_empleado, name='eliminar_empleado'),
]
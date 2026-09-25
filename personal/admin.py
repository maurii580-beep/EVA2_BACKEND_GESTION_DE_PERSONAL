from django.contrib import admin
from .models import Departamento, Cargo, Empleado

# Registro simple para Departamento y Cargo
admin.site.register(Departamento)
admin.site.register(Cargo)

# Personalización del modelo Empleado en el Admin (Requisito de la evaluación)
@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista principal
    list_display = ('rut', 'nombre', 'apellido', 'cargo', 'departamento', 'estado')
    
    # Agregar barra de búsqueda por RUT, Nombre y Apellido
    search_fields = ('rut', 'nombre', 'apellido')
    
    # Agregar filtros laterales por Departamento, Cargo y Estado
    list_filter = ('departamento', 'cargo', 'estado')
    
    # Ordenar por defecto por el apellido
    ordering = ('apellido',)
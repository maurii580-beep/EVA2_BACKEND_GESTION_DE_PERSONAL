from functools import wraps

from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Empleado, Departamento, Cargo
from .forms import EmpleadoForm


def administrador_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapper


# ==========================================
# Inicio del módulo personal
# ==========================================
@login_required
def inicio(request):
    return render(request, 'personal/inicio.html')

# ==========================================
# 1. READ: Listado de empleados (Página Principal)
# ==========================================
@login_required
def lista_empleados(request):
    busqueda = request.GET.get('q', '').strip()
    departamento_id = request.GET.get('departamento', '')
    cargo_id = request.GET.get('cargo', '')
    estado = request.GET.get('estado', '')

    empleados = Empleado.objects.select_related('cargo', 'departamento')
    if busqueda:
        empleados = empleados.filter(
            Q(rut__icontains=busqueda)
            | Q(nombre__icontains=busqueda)
            | Q(apellido__icontains=busqueda)
            | Q(correo_electronico__icontains=busqueda)
            | Q(cargo__nombre_cargo__icontains=busqueda)
            | Q(departamento__nombre__icontains=busqueda)
        )
    if departamento_id.isdigit():
        empleados = empleados.filter(departamento_id=departamento_id)
    else:
        departamento_id = ''
    if cargo_id.isdigit():
        empleados = empleados.filter(cargo_id=cargo_id)
    else:
        cargo_id = ''
    if estado in dict(Empleado.ESTADOS_CHOICES):
        empleados = empleados.filter(estado=estado)
    else:
        estado = ''

    context = {
        'empleados': empleados,
        'departamentos': Departamento.objects.order_by('nombre'),
        'cargos': Cargo.objects.order_by('nombre_cargo'),
        'busqueda': busqueda,
        'departamento_seleccionado': departamento_id,
        'cargo_seleccionado': cargo_id,
        'estado_seleccionado': estado,
        'filtros_activos': any((busqueda, departamento_id, cargo_id, estado)),
    }
    return render(request, 'personal/lista_empleados.html', context)

# ==========================================
# 2. CREATE: Registrar un nuevo empleado
# ==========================================
@administrador_required
def crear_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_empleados')
    else:
        form = EmpleadoForm()
    return render(request, 'personal/form_empleado.html', {'form': form, 'accion': 'Registrar'})

# ==========================================
# 3. READ DETALLE: Vista de detalle completo
# ==========================================
@login_required
def detalle_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    return render(request, 'personal/detalle_empleado.html', {'empleado': empleado})

# ==========================================
# 4. UPDATE: Editar un empleado existente
# ==========================================
@administrador_required
def editar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('lista_empleados')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'personal/form_empleado.html', {'form': form, 'accion': 'Editar'})

# ==========================================
# 5. DELETE: Eliminar un empleado
# ==========================================
@administrador_required
def eliminar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        empleado.delete()
        return redirect('lista_empleados')
    return render(request, 'personal/confirmar_eliminacion.html', {'empleado': empleado})
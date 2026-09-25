from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Empleado, Departamento, Cargo
from .forms import EmpleadoForm

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
    empleados = Empleado.objects.all()
    return render(request, 'personal/lista_empleados.html', {'empleados': empleados})

# ==========================================
# 2. CREATE: Registrar un nuevo empleado
# ==========================================
@login_required
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
@login_required
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
@login_required
def eliminar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        empleado.delete()
        return redirect('lista_empleados')
    return render(request, 'personal/confirmar_eliminacion.html', {'empleado': empleado})
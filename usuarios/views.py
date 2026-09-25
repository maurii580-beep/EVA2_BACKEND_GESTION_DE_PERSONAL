#render permite cargar un archivo HTML.

#redirect permite enviar al usuario a otra página.

from django.shortcuts import render, redirect

#importamos nuestro formulario de registro
from .forms import (
    RegistroUsuarioForm,
    EditarUsuarioForm,
)

from django.contrib.auth.decorators import login_required
# login_required significa que solamente 
# usuarios autenticados pueden acceder.
from personal.models import Empleado, Departamento, Cargo

#Vista responsable del registro de usuarios
def registro_usuario(request):

    # Comprobamos si el navegador está
    # enviando información mediante POST.
    if request.method == 'POST':

        #creamos un formulario utilizando
        #la información que nos envía el navegador
        form = RegistroUsuarioForm(
            request.POST
        )

        #comprobamos si el formulario es válido
        if form.is_valid():
            #guardamos el nuevo usuario en la base de datos
            form.save()

            #redireccionamos al usuario a la página de inicio de sesión
            return redirect('login')

    else:
        #si el navegador no envía información mediante POST
        #entonces creamos un formulario vacío para que el usuario lo complete
        form = RegistroUsuarioForm()

    #mostramos el archivo HTML de registro de usuarios y le pasamos el formulario
    return render(
        request,
        'usuarios/registro.html',
        {
            'form': form,
        }
    )

# Login_required significa que solamente 
# usuarios autenticados pueden acceder a esta vista.
@login_required
def bienvenida(request):
    total_empleados = Empleado.objects.count()
    total_activos = Empleado.objects.filter(estado='Activo').count()
    total_inactivos = Empleado.objects.filter(estado='Inactivo').count()
    total_departamentos = Departamento.objects.count()
    cargos = Cargo.objects.select_related('departamento').order_by('nombre_cargo')
    total_cargos = cargos.count()

    context = {
        'total_empleados': total_empleados,
        'total_activos': total_activos,
        'total_inactivos': total_inactivos,
        'total_departamentos': total_departamentos,
        'total_cargos': total_cargos,
        'cargos': cargos,
    }

    #mostramos el archivo HTML de bienvenida
    return render(
        request,
        'usuarios/bienvenida.html',
        context,
    )

@login_required
def editar_perfil(request):
    # si recibimos información del formulario...
    if request.method == 'POST':

        # request.POST contiene la información que el usuario envió mediante el formulario.
        # instance=request.user indica que
        # modificaremos al usuario actualmente conectado.
        form = EditarUsuarioForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            # guardamos los cambios en la base de datos.
            form.save()

            # redireccionamos al usuario a la página de bienvenida.
            return redirect('bienvenida')

    else:
        # si el navegador no envía información mediante POST,
        # entonces creamos un formulario con los datos del usuario actualmente conectado.
        form = EditarUsuarioForm(
            instance=request.user
        )

    return render(
        request,
        'usuarios/editar_perfil.html',
        {
            'form': form,
        }
    )

@login_required
def eliminar_cuenta(request):

    # por seguridad solamente eliminamos
    # si la peticion utiliza POST.
    if request.method == 'POST':

        # obtenemos al usuario autenticado.
        usuario = request.user

        # Eliminamos el registro.
        usuario.delete()

        # Volvemos al login.
        return redirect('login')

    # si todavia no confirmó,
    # mostamos una página de confirmación.
    return render(
        request,
        'usuarios/eliminar_cuenta.html'
    )
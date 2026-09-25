# Importamos path. 
from django.urls import path

from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)

# Importamos nuestras vistas. 
from . import views

urlpatterns = [
    # Home principal del proyecto
    path(
        '',
        views.bienvenida,
        name='home'
    ),

    # Dirección:
    # 
    # /registro/
    path(
        'registro/',
        views.registro_usuario,
        name='registro'
    ),

    path(
        'login/',
        LoginView.as_view(template_name='usuarios/login.html'),
        name='login'
    ),

    path(
        'bienvenida/',
        views.bienvenida,
        name='bienvenida'
    ),

    path(
        'editar-perfil/',
        views.editar_perfil,
        name='editar_perfil'
    ),

    path(
        'eliminar-cuenta/',
        views.eliminar_cuenta,
        name='eliminar_cuenta'
    ),

    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),


]
from django.contrib import admin

# include permite incorporar
# las urls de otra aplicación.
from django.urls import path, include

urlpatterns = [

    # Django Admin
    path(
        'admin/',
        admin.site.urls
        ),

        #  URLs de nuestra aplicación de usuarios.
        path(
            '',
            include('usuarios.urls')
            ),

        # Conectamos las URLs de nuestra nueva aplicación
        path('personal/', include('personal.urls')),
]
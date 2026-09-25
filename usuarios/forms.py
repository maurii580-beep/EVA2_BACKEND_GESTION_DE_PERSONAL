# Importamos el sistema de formularios de Django. 
from django import forms
# Django ya incorpora un formulario diseñado 
# # especialmente para crear usuarios. 
from django.contrib.auth.forms import UserCreationForm
# Importamos el modelo de usuario incorporado por Django. 
from django.contrib.auth.models import User
# Creamos nuestro formulario de registro. # # Heredamos de 
# UserCreationForm para aprovechar # las validaciones de usuarios y contraseñas 
# # que Django ya incorpora. 
class RegistroUsuarioForm(UserCreationForm):
    # Agregamos el correo electrónico porque
    # queremos solicitarlo obligatoriamente.
    email = forms.EmailField(
        required=True,
        label='Correo electrónico'
    )

    class Meta:
        # Indicamos que este formulario trabaja con el modelo User.
        model = User
        # Definimos los campos que aparecerán en nuestro formulario.
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password1', 
            'password2',
        ]

# Formulario para editar
# datos del usuario.
class EditarUsuarioForm(forms.ModelForm):

    class Meta:

        # Trabajamos con el modelo User.
        model = User

        # Solamente permitiremos modificar
        # estos campos del usuario.
        fields = [
            'first_name', 
            'last_name', 
            'email',
    
        ]
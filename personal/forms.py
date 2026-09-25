from django import forms
from .models import Cargo, Empleado

class EmpleadoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_cargos = Cargo.objects.select_related('departamento').all()

        departamento_id = (
            self.data.get('departamento')
            or self.initial.get('departamento')
            or getattr(self.instance, 'departamento_id', None)
        )
        if departamento_id:
            self.fields['cargo'].queryset = Cargo.objects.filter(departamento_id=departamento_id)
        else:
            self.fields['cargo'].queryset = Cargo.objects.none()

    class Meta:
        model = Empleado
        # Definimos los campos que queremos mostrar en el formulario web
        fields = ['rut', 'nombre', 'apellido', 'correo_electronico', 'telefono', 'fecha_ingreso', 'departamento', 'cargo', 'estado']
        
        # Podemos agregar 'widgets' para mejorar la apariencia en el HTML (opcional pero recomendado)
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
        }
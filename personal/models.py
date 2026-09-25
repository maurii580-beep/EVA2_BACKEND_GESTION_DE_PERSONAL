from django.db import models

# 1. Modelo Departamento
class Departamento(models.Model):
    # Representa las diferentes áreas existentes dentro de la empresa.
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

# 2. Modelo Cargo
class Cargo(models.Model):
    # Representa los distintos cargos que pueden desempeñar los trabajadores.
    nombre_cargo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.RESTRICT, related_name='cargos')

    def __str__(self):
        return self.nombre_cargo

# 3. Modelo Empleado
class Empleado(models.Model):
    # Representa a cada trabajador perteneciente a la empresa[cite: 2].
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo_electronico = models.EmailField()
    telefono = models.CharField(max_length=15)
    fecha_ingreso = models.DateField()
    
    # El estado podrá considerar opciones como Activo o Inactivo[cite: 2].
    ESTADOS_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default='Activo')

    # Relaciones:
    # El campo Cargo deberá establecer una relación con el modelo Cargo[cite: 2].
    cargo = models.ForeignKey(Cargo, on_delete=models.RESTRICT)
    # El campo Departamento deberá establecer una relación con el modelo Departamento[cite: 2].
    departamento = models.ForeignKey(Departamento, on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cargo.nombre_cargo}"
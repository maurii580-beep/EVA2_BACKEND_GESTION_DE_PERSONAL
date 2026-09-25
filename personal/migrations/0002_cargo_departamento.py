from django.db import migrations, models
import django.db.models.deletion


DEPARTAMENTOS = {
    'Gerencia': ['Gerente'],
    'Seguridad': ['Jefe de Seguridad', 'Guardias'],
    'Operaciones': [
        'Jefe de Operaciones',
        'Encargado de Bodega',
        'Encargado de Tesorería',
        'Postventa',
        'Personal de Aseo',
    ],
    'Recursos Humanos': ['Encargado de Recursos Humanos'],
    'Ventas': ['Jefe de Ventas', 'Cajeros'],
}

LEGACY_NAMES = {
    'Gerente': 'Gerente de Tienda',
    'Guardias': 'Guardia',
    'Jefe de Seguridad': 'Jefe Seguridad',
    'Encargado de Tesorería': 'Encargado Tesoría',
    'Postventa': 'Encargado PostVenta',
    'Personal de Aseo': 'Encargado Aseo',
    'Encargado de Recursos Humanos': 'Encargado Recursos Humanos',
    'Cajeros': 'Vendedor',
}


def asignar_cargos_a_departamentos(apps, schema_editor):
    Departamento = apps.get_model('personal', 'Departamento')
    Cargo = apps.get_model('personal', 'Cargo')

    for nombre_departamento, nombres_cargos in DEPARTAMENTOS.items():
        departamento, _ = Departamento.objects.get_or_create(nombre=nombre_departamento)

        for nombre_cargo in nombres_cargos:
            nombre_anterior = LEGACY_NAMES.get(nombre_cargo)
            cargo = None
            if nombre_anterior:
                cargo = Cargo.objects.filter(nombre_cargo=nombre_anterior).first()
            if cargo is None:
                cargo = Cargo.objects.filter(nombre_cargo=nombre_cargo).first()
            if cargo is None:
                cargo = Cargo(nombre_cargo=nombre_cargo)

            cargo.nombre_cargo = nombre_cargo
            cargo.departamento = departamento
            cargo.save()


def revertir_relacion(apps, schema_editor):
    Cargo = apps.get_model('personal', 'Cargo')
    Cargo.objects.update(departamento=None)


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cargo',
            name='departamento',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                related_name='cargos',
                to='personal.departamento',
            ),
        ),
        migrations.RunPython(asignar_cargos_a_departamentos, revertir_relacion),
        migrations.AlterField(
            model_name='cargo',
            name='departamento',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                related_name='cargos',
                to='personal.departamento',
            ),
        ),
    ]

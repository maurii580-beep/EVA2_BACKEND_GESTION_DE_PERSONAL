from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Cargo, Departamento, Empleado


class ListaEmpleadosTests(TestCase):
	def setUp(self):
		usuario = User.objects.create_user(username='gestor', password='test-pass')
		self.client.force_login(usuario)

		self.departamento = Departamento.objects.create(nombre='Ventas')
		self.cargo = Cargo.objects.create(
			nombre_cargo='Vendedor',
			departamento=self.departamento,
		)
		self.empleado = Empleado.objects.create(
			rut='12.345.678-9',
			nombre='Ana',
			apellido='Pérez',
			correo_electronico='ana@example.com',
			telefono='912345678',
			fecha_ingreso=date(2025, 1, 15),
			estado='Activo',
			cargo=self.cargo,
			departamento=self.departamento,
		)

	def test_busqueda_encuentra_por_cargo(self):
		response = self.client.get('/personal/', {'q': 'Vendedor'})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Ana Pérez')
		self.assertEqual(list(response.context['empleados']), [self.empleado])

	def test_filtros_combinados_por_departamento_cargo_y_estado(self):
		response = self.client.get('/personal/', {
			'departamento': self.departamento.id,
			'cargo': self.cargo.id,
			'estado': 'Activo',
		})

		self.assertEqual(response.status_code, 200)
		self.assertEqual(list(response.context['empleados']), [self.empleado])

		response = self.client.get('/personal/', {
			'departamento': self.departamento.id,
			'cargo': self.cargo.id,
			'estado': 'Inactivo',
		})
		self.assertEqual(list(response.context['empleados']), [])

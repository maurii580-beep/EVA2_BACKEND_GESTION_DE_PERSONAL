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


class PermisosGestionPersonalTests(TestCase):
	def setUp(self):
		self.usuario = User.objects.create_user(username='lector', password='test-pass')
		self.client.force_login(self.usuario)
		departamento = Departamento.objects.create(nombre='Ventas')
		cargo = Cargo.objects.create(nombre_cargo='Vendedor', departamento=departamento)
		self.empleado = Empleado.objects.create(
			rut='98.765.432-1',
			nombre='Luis',
			apellido='Rojas',
			correo_electronico='luis@example.com',
			telefono='987654321',
			fecha_ingreso=date(2024, 6, 1),
			cargo=cargo,
			departamento=departamento,
		)

	def test_usuario_normal_solo_puede_ver(self):
		response = self.client.get('/personal/')

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Luis Rojas')
		self.assertNotContains(response, 'Registrar empleado')
		self.assertNotContains(response, 'Editar</a>')
		self.assertNotContains(response, 'Eliminar</a>')

	def test_usuario_normal_no_puede_crear_editar_ni_eliminar(self):
		response = self.client.get('/personal/crear/')
		self.assertEqual(response.status_code, 403)

		response = self.client.post(f'/personal/editar/{self.empleado.id}/', {})
		self.assertEqual(response.status_code, 403)

		response = self.client.post(f'/personal/eliminar/{self.empleado.id}/', {})
		self.assertEqual(response.status_code, 403)
		self.assertTrue(Empleado.objects.filter(id=self.empleado.id).exists())

	def test_administrador_staff_puede_abrir_formularios(self):
		administrador = User.objects.create_user(
			username='admin-personal',
			password='test-pass',
			is_staff=True,
		)
		self.client.force_login(administrador)

		self.assertEqual(self.client.get('/personal/crear/').status_code, 200)
		self.assertEqual(self.client.get(f'/personal/editar/{self.empleado.id}/').status_code, 200)
		self.assertEqual(self.client.get(f'/personal/eliminar/{self.empleado.id}/').status_code, 200)

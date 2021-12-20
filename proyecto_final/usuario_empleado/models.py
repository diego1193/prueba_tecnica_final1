# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class UsuarioEmpleado(AbstractBaseUser):
    id_empleado = models.AutoField(primary_key=True)
    cedula_empleado = models.IntegerField(blank=True, null=True)
    nombre_empleado = models.TextField(blank=True, null=True)
    email_empleado = models.TextField(blank=True, null=True)
    usuario_empleado = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    telefono_empleado = models.TextField(blank=True, null=True)
    estado_empleado_empresa = models.TextField(blank=True, null=True)
    last_login = models.TextField(blank=True, null=True)
    validacion_empleado = models.IntegerField(blank=True, null=True)
    empresa = models.TextField(blank=True, null=True)
    fecha_validacion = models.TextField(blank=True, null=True)
    geolocalizacion_login = models.TextField(blank=True, null=True)
    username = None

    USERNAME_FIELD = "email_empleado"
    REQUIRED_FIELDS = []

    class Meta:
        managed = False
        db_table = 'USUARIO_EMPLEADO'


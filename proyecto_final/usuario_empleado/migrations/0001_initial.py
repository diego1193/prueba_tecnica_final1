# Generated by Django 3.1.7 on 2021-12-19 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioEmpleado',
            fields=[
                ('id_empleado', models.AutoField(primary_key=True, serialize=False)),
                ('cedula_empleado', models.IntegerField(blank=True, null=True)),
                ('nombre_empleado', models.TextField(blank=True, null=True)),
                ('email_empleado', models.TextField(blank=True, null=True)),
                ('usuario_empleado', models.TextField(blank=True, null=True)),
                ('password', models.TextField(blank=True, null=True)),
                ('telefono_empleado', models.TextField(blank=True, null=True)),
                ('estado_empleado_empresa', models.TextField(blank=True, null=True)),
                ('last_login', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'USUARIO_EMPLEADO',
                'managed': False,
            },
        ),
    ]

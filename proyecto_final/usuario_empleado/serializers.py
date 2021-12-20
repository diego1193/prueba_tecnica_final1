from rest_framework import serializers
from .models import UsuarioEmpleado

class UsuarioEmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioEmpleado
        fields = ["id_empleado", "cedula_empleado", "nombre_empleado",
                  "email_empleado", "usuario_empleado", "password", "telefono_empleado",
                  "estado_empleado_empresa", 'validacion_empleado', "empresa", "fecha_validacion", "geolocalizacion_login"]

        extra_kwards = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password_propietario = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password_propietario is not None:
            instance.set_password(password_propietario)
        instance.save()
        return instance
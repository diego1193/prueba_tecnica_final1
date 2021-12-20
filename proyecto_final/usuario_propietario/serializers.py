from django.db.models import fields
from rest_framework import serializers
from .models import UsuarioPropietario

class UsuarioPropietarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioPropietario
        fields = ['id_propietario','cedula_propietario', 'nombre_propietario', 'email_propietario', 'usuario_propietario',
                  'password', 'telefono_propietario']
        extra_kwards = {
            'password': {'write_only': True} #Para que cuando retorne no me muestre la contraseña
        }
    
    #! Se crea el hash o la contraseña unica
    def create(self, validated_data):
        password_propietario = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password_propietario is not None:
            instance.set_password(password_propietario)
        instance.save()
        return instance
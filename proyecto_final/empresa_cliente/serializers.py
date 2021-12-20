from django.db.models import fields
from rest_framework import serializers
from .models import EmpresaCliente

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpresaCliente
        fields = ("nit_c", "nombre_empresa_c", "nombre_comercial_c", 
                 "telefono_c", "direccion_c", "user_admin_c", "email_c",
                 "web_c", "pais_c", "estado_c", "ciudad_c")
from django.db.models import fields
from rest_framework import serializers
from .models import EmpresaPropietario

class EmpresaPropietarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpresaPropietario
        fields = ("nit_p", "nombre_empresa_p", "nombre_comercial_p", 
                 "telefono_p", "direccion_p", "user_admin_p", "email_p",
                 "web_p", "pais_p", "estado_p", "ciudad_p")
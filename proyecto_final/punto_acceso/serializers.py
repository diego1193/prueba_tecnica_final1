from django.db.models import fields
from rest_framework import serializers
from .models import PuntoAcceso

class PuntoAccesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuntoAcceso
        fields = ("id_access", "nombre_empresa", "geolocalizacion", 
                 "email", "estado", "direccion")
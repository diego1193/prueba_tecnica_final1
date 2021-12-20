from django.shortcuts import render
import jwt, datetime, re, validators
from rest_framework import serializers
from rest_framework import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from usuario_propietario.models import UsuarioPropietario
from usuario_propietario.serializers import UsuarioPropietarioSerializer

from .serializers import ClienteSerializer
from .models import EmpresaCliente

def check_email(email):
    regex_my = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if(re.search(regex_my, email)):
        return 1
    else:
        return 0

class RegisterClienteViews(APIView):
    def post(self, request):

        token = request.COOKIES.get("jwt")

        #Si no es autentico
        if not token:
            raise AuthenticationFailed("Unauthenticated")

        #Intente decodificar el token y cagarlo en la carga util (payload)
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
            #print(payload['id'])
            user_id = UsuarioPropietario.objects.filter(id_propietario=payload['id']).first()
            serializerUserId = UsuarioPropietarioSerializer(user_id)
            #print(serializerUserId.data)

            if serializerUserId.data["cedula_propietario"] == None:
                return Response({"Message": "Token invalidado"})
        except:
            raise AuthenticationFailed("Unauthenticated")

        data = request.data
        ###Chequear Email ###3
        check_e = check_email(data["email_c"])

        if check_e == 1:
            pass
        elif check_e == 0:
            return Response({"message": "Correo invalido"})
        
        ###Chequear web ###
        check_web = validators.url(data["web_c"])
        if check_web != True:
            return Response({"message": "Direccion web invalida"})
        
        serializer = ClienteSerializer(data=data)
        if serializer.is_valid():
            empresas = EmpresaCliente.objects.values()
            for empresa in empresas:
                if empresa["nit_c"] == serializer.validated_data.get("nit_c"):
                    return Response({"Message": "Empresa Registrada"})
            serializer.save()
        return Response(serializer.data)

class ReadClientesViews(APIView):
    def get(self, request):

        token = request.COOKIES.get("jwt")
        #Si no es autentico
        if not token:
            raise AuthenticationFailed("Unauthenticated")
            
        #Intente decodificar el token y cagarlo en la carga util (payload)
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
            print(payload['id'])
            user_id = UsuarioPropietario.objects.filter(id_propietario=payload['id']).first()
            serializerUserId = UsuarioPropietarioSerializer(user_id)
            print(serializerUserId.data)

            if serializerUserId.data["cedula_propietario"] == None:
                return Response({"Message": "Token invalidado"})
        except:
            raise AuthenticationFailed("Unauthenticated")
        
        cliente = EmpresaCliente.objects.values()
        list_cliente = [clientes for clientes in cliente]

        response_query = list_cliente

        return Response(response_query)

class ReadClientesViewsIndividual(APIView):
    def get(self, request, nit):
        token = request.COOKIES.get("jwt")
        #print("Nit", nit)

        #Si no es autentico
        if not token:
            raise AuthenticationFailed("Unauthenticated")
            
        #Intente decodificar el token y cagarlo en la carga util (payload)
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
            #print(payload['id'])
            user_id = UsuarioPropietario.objects.filter(id_propietario=payload['id']).first()
            serializerUserId = UsuarioPropietarioSerializer(user_id)
            #print(serializerUserId.data)

            if serializerUserId.data["cedula_propietario"] == None:
                return Response({"Message": "Token invalidado"})
        except:
            raise AuthenticationFailed("Unauthenticated")
        
        clientes = EmpresaCliente.objects.values()
        list_cliente = [cliente for cliente in clientes if cliente["nit_c"]==int(nit)]

        if list_cliente == []:
            return Response({"message": "No hay datos sobre la empresa"})
        
        response_query = list_cliente

        return Response(response_query)

class UpdateClienteView(APIView):
    def post(self, request):

        token = request.COOKIES.get("jwt")

        #Si no es autentico
        if not token:
            raise AuthenticationFailed("Unauthenticated")
        #Intente decodificar el token y cagarlo en la carga util (payload)
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
            print(payload['id'])
            user_id = UsuarioPropietario.objects.filter(id_propietario=payload['id']).first()
            serializerUserId = UsuarioPropietarioSerializer(user_id)
            print(serializerUserId.data)

            if serializerUserId.data["cedula_propietario"] == None:
                return Response({"Message": "Token invalidado"})
        except:
            raise AuthenticationFailed("Unauthenticated")
        #Traemos el usuario
        data = request.data

        check_e = check_email(data["email_c"])

        if check_e == 1:
            pass
        elif check_e == 0:
            return Response({"message": "Correo invalido"})

        check_web = validators.url(data["web_c"])
        if check_web != True:
            return Response({"message": "Direccion web invalida"})

        clientes = EmpresaCliente.objects.values()
        cliente1 = [cliente for cliente in clientes if cliente["nit_c"]==data["nit_c"]]

        list_cliente = [[clave, valor] for clave, valor in data.items()]

        try:
            list_cliente_query = [[clave, valor] for clave, valor in cliente1[0].items()]
        except:
            return Response({"message":"No se puede modificar el Nit"})
        
        dict_response = {}
        for l in range(len(list_cliente_query)-1):
            listC = list_cliente[l]
            listQ = list_cliente_query[l]
            if (listC[1]==listQ[1]) or (listC[1]==""):
                dict_response[listQ[0]] = listQ[1]
            elif(listC[1]!=listQ[1]):
                dict_response[listC[0]] = listC[1]
        
        serializer = ClienteSerializer(data=data)
        if serializer.is_valid():
            clientes = EmpresaCliente.objects.values()
            for cliente in clientes:
                if cliente["nit_c"] == serializer.validated_data.get("nit_c"):
                    id_old = cliente["id_c"]
            serializer.save()
            try:
                EmpresaCliente.objects.filter(id_c=id_old).first().delete()
            except:
                return Response(serializer.data)
        return Response(serializer.data)

class DeleteClienteViews(APIView):
    def get(self, request, nit):

        token = request.COOKIES.get("jwt")
        #print("Nit", nit)

        #Si no es autentico
        if not token:
            raise AuthenticationFailed("Unauthenticated")
            
        #Intente decodificar el token y cagarlo en la carga util (payload)
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
            #print(payload['id'])
            user_id = UsuarioPropietario.objects.filter(id_propietario=payload['id']).first()
            serializerUserId = UsuarioPropietarioSerializer(user_id)
            #print(serializerUserId.data)

            if serializerUserId.data["cedula_propietario"] == None:
                return Response({"Message": "Token invalidado"})
        except:
            raise AuthenticationFailed("Unauthenticated")
        
        try:
            EmpresaCliente.objects.filter(nit_c=int(nit)).first().delete()
        except:
            return Response({"message": "Empresa no existe"})
        #print(list_empresa)

        response_query = {"mesaage": "Eliminada correctamete"}


        return Response(response_query)
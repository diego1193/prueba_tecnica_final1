from django.shortcuts import render
import jwt, datetime, re, validators
from rest_framework import serializers
from rest_framework import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from usuario_propietario.models import UsuarioPropietario
from usuario_propietario.serializers import UsuarioPropietarioSerializer

from .serializers import EmpresaPropietarioSerializer
from .models import EmpresaPropietario
# Create your views here.

def check_email(email):
    regex_my = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if(re.search(regex_my, email)):
        return 1
    else:
        return 0


class RegisterEmpresaView(APIView):
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

        data = request.data

        ###Chequear Email ###3
        check_e = check_email(data["email_p"])

        if check_e == 1:
            pass
        elif check_e == 0:
            return Response({"message": "Correo invalido"})

        ###Chequear web ###
        check_web = validators.url(data["web_p"])
        if check_web != True:
            return Response({"message": "Direccion web invalida"})

        serializer = EmpresaPropietarioSerializer(data=request.data)
        user = UsuarioPropietario.objects.filter(nombre_propietario=data['user_admin_p']).first()
        serializerUser = UsuarioPropietarioSerializer(user)

        if serializerUser.data["cedula_propietario"] == None:
            return Response({"Message": "Propietario aún no se ha registrado"})
        print(serializerUser.data)
        if serializer.is_valid():
            empresas = EmpresaPropietario.objects.values()
            for empresa in empresas:
                if empresa["nit_p"] == serializer.validated_data.get("nit_p"):
                    return Response({"Message": "Empresa Registrada"})
            serializer.save()
        return Response(serializer.data)

class ReadEmpresaProViews(APIView):
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
        
        #Traemos el usuario
        #user = UsuarioPropietario.objects.filter(id_propietario=payload['id']).first()
        empresas = EmpresaPropietario.objects.values()
        list_empresa = [empresa for empresa in empresas]

        #serializer = UsuarioPropietarioSerializer(user)
        
        
        #serializer = UsuarioPropietarioSerializerRead(user)

        response_query = list_empresa


        return Response(response_query)

class ReadEmpresaProViewsIndiviual(APIView):
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
        
        #Traemos el usuario
        empresas = EmpresaPropietario.objects.values()
        list_empresa = [empresa for empresa in empresas if empresa["nit_p"]==int(nit)]

        if list_empresa == []:
            return Response({"message": "No hay datos sobre la empresa"})
        #print(list_empresa)

        response_query = list_empresa


        return Response(response_query)

class UpdateEmpresaProView(APIView):
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

        check_e = check_email(data["email_p"])

        if check_e == 1:
            pass
        elif check_e == 0:
            return Response({"message": "Correo invalido"})

        check_web = validators.url(data["web_p"])
        if check_web != True:
            return Response({"message": "Direccion web invalida"})

        empresas = EmpresaPropietario.objects.values()
        empresa1 = [empresa for empresa in empresas if empresa["nit_p"]==data["nit_p"]]

        list_empresa = [[clave, valor] for clave, valor  in data.items()]
        try:
            list_empresa_query = [[clave, valor] for clave, valor in empresa1[0].items()]
        except:
            return Response({"message":"No se puede modificar el Nit"})

        dict_response = {}
        for l in range(len(list_empresa_query)-1):
            listE = list_empresa[l]
            listQ = list_empresa_query[l+1]
            if (listE[1]==listQ[1]) or (listE[1]==""):
                dict_response[listQ[0]] = listQ[1]
            elif(listE[1]!=listQ[1]):
                dict_response[listE[0]] = listE[1]


        serializer = EmpresaPropietarioSerializer(data=request.data)
        user = UsuarioPropietario.objects.filter(nombre_propietario=data['user_admin_p']).first()
        serializerUser = UsuarioPropietarioSerializer(user)

        if serializerUser.data["cedula_propietario"] == None:
            return Response({"Message": "Propietario aún no se ha registrado"})
        print(serializerUser.data)
        if serializer.is_valid():
            empresas = EmpresaPropietario.objects.values()
            for empresa in empresas:
                if empresa["nit_p"] == serializer.validated_data.get("nit_p"):
                    id_old = empresa["id_p"]
            serializer.save()
            try:
                EmpresaPropietario.objects.filter(id_p=id_old).first().delete()
            except:
                return Response(serializer.data)
        return Response(serializer.data)


class DeleteEmpresaProViewsIndiviual(APIView):
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
            EmpresaPropietario.objects.filter(nit_p=int(nit)).first().delete()
        except:
            return Response({"message": "Empresa no existe"})
        #print(list_empresa)

        response_query = {"mesaage": "Eliminada correctamete"}


        return Response(response_query)
import jwt, datetime, re
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .serializers import UsuarioPropietarioSerializer
from .models import UsuarioPropietario
# Create your views here.

def check_email(email):
    regex_my = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if(re.search(regex_my, email)):
        return 1
    else:
        return 0


class RegisterUserProView(APIView):
    def post(self, request):

        data = request.data

        ###Chequear Email ###3
        check_e = check_email(data["email_propietario"])

        if check_e == 1:
            pass
        elif check_e == 0:
            return Response({"message": "Correo invalido"})
        
        #Verificamos el serializador, si no existe queremos borramos los datos y la excepcion
        user = UsuarioPropietario.objects.filter(cedula_propietario=data['cedula_propietario']).first()
        serializer = UsuarioPropietarioSerializer(user)

        if data["cedula_propietario"] == serializer.data["cedula_propietario"]:
            return Response({"Message": "Usuario Existente"})

        if serializer.data["cedula_propietario"]==None:
            serializer = UsuarioPropietarioSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(serializer.data)


class LoginUserProView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user= UsuarioPropietario.objects.filter(email_propietario=email).first() #Si el email es igual al correo registrado, traigame el primero

        if user is None:
            raise AuthenticationFailed("!User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload={
            "id": user.id_propietario,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60), #Hora de expiracion del token
            "iat": datetime.datetime.utcnow() #Hora q genera el token
        }

        #Codificacion del token
        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()
        
        #Cookies
        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'jwt': token
        }

        return response


class ReadProViews(APIView):
    def get(self, request):

        token = request.COOKIES.get("jwt")

        #Si no es autentico
        if not token:
            raise AuthenticationFailed("Unauthenticated")
        
        #Intente decodificar el token y cagarlo en la carga util (payload)
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
            if payload["id"] == None:
                return(Response({"message": "No tiene acceso"}))
        except:
            raise AuthenticationFailed("Unauthenticated")
        
        #Traemos el usuario
        #user = UsuarioPropietario.objects.filter(id_propietario=payload['id']).first()
        user = UsuarioPropietario.objects.values()
        list_user = [users for users in user]
        print(list_user)
        #serializer = UsuarioPropietarioSerializer(user)
        
        
        #serializer = UsuarioPropietarioSerializerRead(user)

        response_query = list_user


        return Response(response_query)

class ReadProViewsIndividual(APIView):
    def get(self, request):

        token = request.COOKIES.get("jwt")

        #Si no es autentico
        if not token:
            raise AuthenticationFailed("Unauthenticated")
        
        #Intente decodificar el token y cagarlo en la carga util (payload)
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
            if payload["id"] == None:
                return(Response({"message": "No tiene acceso"}))
        except:
            raise AuthenticationFailed("Unauthenticated")
        
        #Traemos el usuario
        user = UsuarioPropietario.objects.filter(id_propietario=payload['id']).first()
        serializer = UsuarioPropietarioSerializer(user)

        response_query = serializer.data


        return Response(response_query)

class UpdateProView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated")
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
            if payload["id"] == None:
                return(Response({"message": "No tiene acceso"}))

        except:
            raise AuthenticationFailed("Unauthenticated")
        #Traemos el usuario
        data = request.data

        ###Chequear Email ###3
        check_e = check_email(data["email_propietario"])

        if check_e == 1:
            pass
        elif check_e == 0:
            return Response({"message": "Correo invalido"})

        user = UsuarioPropietario.objects.filter(id_propietario=payload['id']).first()
        serializer = UsuarioPropietarioSerializer(user)
        response_query = serializer.data

        id_data = payload["id"]

        list_user = [[clave, valor]for clave, valor in data.items()]
        list_response_query = [[clave, valor] for clave, valor in response_query.items()]
        #print("Query",list_response_query)

        #UsuarioPropietario.objects.filter(id_propietario=payload['id']).first().delete()

        #print("Id", id_data)
        dict_response = {"id_propietario": id_data}
        for l in range(len(list_response_query)-1):
            listU = list_user[l]
            listR = list_response_query[l+1]
            if (listU[1] == listR[1]) or (listU[1]==""):
                dict_response[listR[0]] = listR[1]
            elif(listU[1]!=listR[1]):
                dict_response[listR[0]] = listU[1]
        #print(response_query["cedula_propietario"])
        
        #print("Diccionario",dict_response)
        
        serializer_new = UsuarioPropietarioSerializer(data=dict_response)
        serializer_new.is_valid(raise_exception=True)#Verificamos el serializador, si no existe queremos borramos los datos y la excepcion
        serializer_new.save()

        user_last = UsuarioPropietario.objects.latest('id_propietario')
        user_last = UsuarioPropietarioSerializer(user_last)
        user_last_query = user_last.data

        #print("Ultimo usuario registrado", user_last_query)

        UsuarioPropietario.objects.filter(id_propietario=id_data).first().delete()
        
        response = Response()

        response.delete_cookie('jwt')

        payload={
            "id": user_last_query["id_propietario"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60), #Hora de expiracion del token
            "iat": datetime.datetime.utcnow() #Hora q genera el token
        }

        #Codificacion del token
        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()
        
        #Cookies
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = serializer_new.data

        
        return response

class LogoutUserProView(APIView):
    def get(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

class EliminarCuentaViews(APIView):
    def get(self, request):

        token = request.COOKIES.get("jwt")

        #Si no es autentico
        if not token:
            raise AuthenticationFailed("Unauthenticated")


        #Intente decodificar el token y cagarlo en la carga util (payload)
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
            if payload["id"] == None:
                return(Response({"message": "No tiene acceso"}))
        except:
            raise AuthenticationFailed("Unauthenticated")

        #Traemos el usuario
        UsuarioPropietario.objects.filter(id_propietario=payload['id']).first().delete()

        response = Response()
        response.delete_cookie('jwt')

        response.data = {
            "message": "Cuenta eliminada correctamente"
        }

        return response



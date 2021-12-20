import pandas as pd
from datetime import datetime as time
import jwt, re, requests, json
from django.shortcuts import render
from rest_framework import serializers
from rest_framework import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .serializers import UsuarioEmpleadoSerializer
from .models import UsuarioEmpleado
from empresa_propietario.models import EmpresaPropietario
from empresa_propietario.serializers import EmpresaPropietarioSerializer
from django.http.response import JsonResponse
from .tests import send_email, send_email_error
import datetime


def check_email(email):
    regex_my = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if(re.search(regex_my, email)):
        return 1
    else:
        return 0

class RegisterUserEmpleadoView(APIView):
    def post(self, request):

        data = request.data

        ###Chequear Email ###3
        check_e = check_email(data["email_empleado"])

        if check_e == 1:
            pass
        elif check_e == 0:
            return Response({"message": "Correo invalido"})

        data["estado_empleado_empresa"] = "Activo"
        data["validacion_empleado"] = 0
        data["fecha_validacion"] = "2025-12-24-1-1-0-24"

        #Verificamos el serializador, si no existe queremos borramos los datos y la excepcion
        user = UsuarioEmpleado.objects.filter(cedula_empleado=data['cedula_empleado']).first()
        serializer = UsuarioEmpleadoSerializer(user)

        userE = UsuarioEmpleado.objects.filter(email_empleado=data['email_empleado']).first()
        serializerE = UsuarioEmpleadoSerializer(userE)

        userU = UsuarioEmpleado.objects.filter(usuario_empleado=data['usuario_empleado']).first()
        serializerU = UsuarioEmpleadoSerializer(userU)

        if data["cedula_empleado"] == serializer.data["cedula_empleado"]:
            return Response({"Message": "Usuario ya esta registrado"})

        if data["email_empleado"] == serializerE.data["email_empleado"]:
            return Response({"Message": "Correo existente"})
        
        if data['usuario_empleado'] == serializerU.data["usuario_empleado"]:
            return Response({"Message": "Usuario ya existe"})

        if serializer.data["cedula_empleado"]==None:
            serializer = UsuarioEmpleadoSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(serializer.data)

class ValidacionUserViews(APIView):

    def get(self, request, correo):

        user = UsuarioEmpleado.objects.filter(usuario_empleado=correo).first()
        serializer = UsuarioEmpleadoSerializer(user)

        if user is None:
            raise AuthenticationFailed("!User not found!")

        UsuarioEmpleado.objects.filter(cedula_empleado=serializer.data["cedula_empleado"]).update(validacion_empleado=1)

        return JsonResponse({"message": "Validacion correcta"})

class SendEmailValidacionView(APIView):

    def post(self, request):

        dataE = request.data

        userE = UsuarioEmpleado.objects.filter(email_empleado=dataE["email"]).first()
        serializerE = UsuarioEmpleadoSerializer(userE)

        if userE is None:
            raise AuthenticationFailed("!User not found!")
        


        url = f"http://127.0.0.1:8002/api/validacionEmpleado/{serializerE.data['usuario_empleado']}"
        """
        datos = {
            "email": serializerE.data["email_empleado"]
        }
        respuesta = requests.put(url, json=datos)
        """
        send_email(serializerE.data["email_empleado"], url)

        #print(respuesta)

        return Response({"Message": "ok"})

class LoginUserEmpleado(APIView):
    def post(self, request):
        
        data = request.data

        emailU = data["email_empleado"]
        passwordU = data["password"]

        now = time.now()
        date = now.date()
        temp = pd.Timestamp(date)
        dayOfWeek = temp.dayofweek
        hour = now.hour
        day_hour = str(date) + f"-{dayOfWeek}-{hour}"

        print(f"Dia de la semana {dayOfWeek}, hora {hour}, fecha {day_hour}")

        user = UsuarioEmpleado.objects.filter(email_empleado=emailU).first()


        if user is None:
            raise AuthenticationFailed("¡Usuario no encontrado!")

        if not user.check_password(passwordU):

            serializerUser = UsuarioEmpleadoSerializer(user)
            nombreEmp = serializerUser.data["nombre_empleado"].upper()
            empresa1 = serializerUser.data["empresa"].upper()
            pEmpresa = EmpresaPropietario.objects.values()
            #print(pEmpresa)
            try:
                list_empresa = [empresa for empresa in pEmpresa if empresa["nombre_empresa_p"].upper()==empresa1][0]
            except:
                return Response({"message": "El usuario se registro con una empresa no registrada"})
            emailEmpresa = list_empresa["email_p"]
            send_email_error(emailEmpresa, nombreEmp, empresa1)
            print(emailEmpresa)
            raise AuthenticationFailed("Incorrect password!")

        serializer = UsuarioEmpleadoSerializer(user)

        if serializer.data["validacion_empleado"] == 0:
            response = Response()
            response.data = {
                "message":"Usuario no se ha validado"
            }
            return response

        activacion = 1
        estado = "Activo"

        dict_response_inv = {"message": "No tienes permiso para ingresar, por favor contactate con el administrador"}
        date_validation = serializer.data["fecha_validacion"].split("-")
        day_hour1 = day_hour.split("-")
        if int(day_hour1[0]) > int(date_validation[0]):
            activacion = 0
        elif int(day_hour1[0]) == int(date_validation[0]) and int(day_hour1[1])>int(date_validation[1]):
            activacion = 0
        elif int(day_hour1[0]) == int(date_validation[0]) and int(day_hour1[1]) >= int(date_validation[1]) and int(day_hour1[2]) > int(date_validation[2]):
            activacion = 0

        print(day_hour1[3])
        
        if (int(date_validation[3]) == 1) and (0<=int(day_hour1[3])<=4):
            if int(day_hour1[4]) not in range(int(date_validation[5]), int(date_validation[6])):
                activacion = 0

        elif (int(date_validation[3]) == 0) and (0<=int(day_hour1[3])<=4):
            activacion = 0
        
        if (int(date_validation[4]) == 1) and (5<=int(day_hour1[3])<=6):
            if int(day_hour1[4]) not in range(int(date_validation[5]), int(date_validation[6])):
                activacion = 0
        elif (int(date_validation[4]) == 0) and (int(day_hour1[3])==6):
            activacion = 0


        payload={
            "act": activacion,
            "usr": user.usuario_empleado,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60), #Hora de expiracion del token
            "iat": datetime.datetime.utcnow() #Hora q genera el token
        }

        #Codificacion del token
        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()

        #Cookies
        response.set_cookie(key='jwt', value=token, httponly=True)


        #print(date_validation)
        if activacion == 0:
            estado = "Desactivo"
            UsuarioEmpleado.objects.filter(email_empleado=emailU).update(last_login=day_hour)
            UsuarioEmpleado.objects.filter(email_empleado=emailU).update(estado_empleado_empresa=estado)
            response.data = dict_response_inv
        elif activacion == 1:
            UsuarioEmpleado.objects.filter(email_empleado=emailU).update(estado_empleado_empresa=estado)
            UsuarioEmpleado.objects.filter(email_empleado=emailU).update(last_login=day_hour)
            response.data = {
                'jwt': token
            }

        return response

class UploadUserEmpleado(APIView):
    def post(self, request):

        token = request.COOKIES.get("jwt")

        #Si no es autentico
        if not token:
            raise AuthenticationFailed("Unauthenticated")
        #Intente decodificar el token y cagarlo en la carga util (payload)
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
            print(payload['usr'])
            user_empleado =  UsuarioEmpleado.objects.filter(usuario_empleado=payload['usr']).first()
            serializerUserempleado = UsuarioEmpleadoSerializer(user_empleado)
            print(serializerUserempleado.data)

            if serializerUserempleado.data["cedula_empleado"] == None:
                return Response({"Message": "Token invalidado"})
        except:
            raise AuthenticationFailed("Unauthenticated")

        data = request.data

        now = time.now()
        date = now.date()
        temp = pd.Timestamp(date)
        dayOfWeek = temp.dayofweek
        hour = now.hour
        day_hour = str(date) + f"-{dayOfWeek}-{hour}"

        print(f"Dia de la semana {dayOfWeek}, hora {hour}, fecha {day_hour}")


        user = UsuarioEmpleado.objects.filter(email_empleado=data["email_empleado"]).first()
        serializer = UsuarioEmpleadoSerializer(user)
        if user is None:
            raise AuthenticationFailed("No puedes actualizar el correo, contacta al administrador")

        if serializer.data["validacion_empleado"] == 0:
            response = Response()
            response.data = {
                "message":"Usuario no se ha validado"
            }
            return response

        activacion = 1
        estado = "Activo"

        dict_response_inv = {"message": "No tienes permiso para ingresar, por favor contactate con el administrador"}
        date_validation = serializer.data["fecha_validacion"].split("-")
        day_hour1 = day_hour.split("-")
        if int(day_hour1[0]) > int(date_validation[0]):
            activacion = 0
        elif int(day_hour1[0]) == int(date_validation[0]) and int(day_hour1[1])>int(date_validation[1]):
            activacion = 0
        elif int(day_hour1[0]) == int(date_validation[0]) and int(day_hour1[1]) >= int(date_validation[1]) and int(day_hour1[2]) > int(date_validation[2]):
            activacion = 0

        print(day_hour1[3])
        
        if (int(date_validation[3]) == 1) and (0<=int(day_hour1[3])<=4):
            if int(day_hour1[4]) not in range(int(date_validation[5]), int(date_validation[6])):
                activacion = 0

        elif (int(date_validation[3]) == 0) and (0<=int(day_hour1[3])<=4):
            activacion = 0
        
        if (int(date_validation[4]) == 1) and (5<=int(day_hour1[3])<=6):
            if int(day_hour1[4]) not in range(int(date_validation[5]), int(date_validation[6])):
                activacion = 0
        elif (int(date_validation[4]) == 0) and (int(day_hour1[3])==6):
            activacion = 0

        response = Response()

        #print(date_validation)
        if activacion == 0:
            response.data = dict_response_inv
            return response

        response_query=serializer.data
        list_keys_response =[[clave, valor] for clave, valor in response_query.items() if clave not in ["cedula_empleado",
                                 "nombre_empleado", "email_empleado", "usuario_empleado", "password","telefono_empleado", "empresa"]]

        id_data = serializer.data["id_empleado"]

        list_user = [[clave, valor]for clave, valor in data.items()]
        list_response_query = [[clave, valor] for clave, valor in response_query.items() 
                                if clave in ["cedula_empleado", "nombre_empleado", "email_empleado",
                                "usuario_empleado", "password","telefono_empleado", "empresa"]]
        #print("Query",list_response_query)

        #UsuarioPropietario.objects.filter(id_propietario=payload['id']).first().delete()

        #print("Id", id_data)
        dict_response = {}
        #print("QUERYYY",list_user)
        #print("",list_response_query)

        for l in range(len(list_response_query)):
            listU = list_user[l]
            listR = list_response_query[l]
            if (listU[1] == listR[1]) or (listU[1]==""):
                dict_response[listR[0]] = listR[1]
            elif(listU[1]!=listR[1]):
                if listR[0] == "email_empleado" or listR[0] == "usuario_empleado":
                    return Response({"message": "No puedes cambiar el usuario, contacta al administrador"})
                dict_response[listR[0]] = listU[1]
        
        dict_response1 = dict_response

        for i in range(len(list_keys_response)):
            dict_response[list_keys_response[i][0]] = list_keys_response[i][1]
        
    
        serializer_new = UsuarioEmpleadoSerializer(data=dict_response)
        serializer_new.is_valid(raise_exception=True)#Verificamos el serializador, si no existe queremos borramos los datos y la excepcion
        serializer_new.save()

        user_last = UsuarioEmpleado.objects.latest('id_empleado')
        user_last = UsuarioEmpleadoSerializer(user_last)
        user_last_query = user_last.data

        UsuarioEmpleado.objects.filter(id_empleado=id_data).first().delete()
        
        response = Response()

        response.delete_cookie('jwt')

        payload={
            "act": activacion,
            "usr": user.usuario_empleado,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60), #Hora de expiracion del token
            "iat": datetime.datetime.utcnow() #Hora q genera el token
        }

        #Codificacion del token
        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()
        
        #Cookies
        response.set_cookie(key='jwt', value=token, httponly=True)
        
        #response.data = serializer_new.data
        response = Response()
        response.data = dict_response1
        
        return response

class DeleteUserView(APIView):
    def get(self, request, cedula):


        #Traemos el usuario
        try:
            UsuarioEmpleado.objects.filter(cedula_empleado=cedula).first().delete()
        except:
            return Response({"message": "No existe usuario"})
        response = Response()
        response.delete_cookie('jwt')

        response.data = {
            "message": "Cuenta eliminada correctamente"
        }

        return response









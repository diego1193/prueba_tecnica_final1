from django.shortcuts import render
import jwt, datetime, re, validators, ast
from rest_framework import serializers
from rest_framework import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from geopy.geocoders import Nominatim


from usuario_propietario.models import UsuarioPropietario
from usuario_propietario.serializers import UsuarioPropietarioSerializer

from empresa_propietario.models import EmpresaPropietario
from empresa_propietario.serializers import EmpresaPropietario, EmpresaPropietarioSerializer

from .serializers import PuntoAccesoSerializer
from .models import PuntoAcceso


def check_email(email):
    regex_my = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if(re.search(regex_my, email)):
        return 1
    else:
        return 0

def geolocalizacion(direccion):
    geolocator = Nominatim(user_agent="proyecto")
    location = geolocator.geocode(direccion)
    return location.raw

class RegisterPuntoAccesoViews(APIView):
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
        check_e = check_email(data["email"])

        if check_e == 1:
            pass
        elif check_e == 0:
            return Response({"message": "Correo invalido"})
        
        direccion_finalList = []
        direccion = data["direccion"].split()
        #direccion = re.split("[#-]", direccion)
        direccion = [re.split("[#-]", direc) for direc in direccion]
        for d in range(len(direccion)):
            dirc = direccion[d]
            extraer = [di for di in dirc if di != '']
            if extraer != []:
                if d == 3 or d == 2:
                    direccion_finalList.append(',')
                for ex in range(len(extraer)):
                    concatenar = extraer[ex]
                    direccion_finalList.append(concatenar)
        direccion_finalList.append(",")
        direccion_finalList.append(data["ciudad"])
        
        direccion_final = " ".join(direccion_finalList)
        
        geo1 = {}
        try:
            geo = geolocalizacion(direccion_final)
        except:
            return Response({"Message": "No existe direccion"})
        geo1["lat"] = geo["lat"]
        geo1["lon"] = geo["lon"]
        geo1["info"] = geo["display_name"]

        data["geolocalizacion"] = f"{geo1}"


        serializer_acceso = PuntoAccesoSerializer(data=data)
        empresas = EmpresaPropietario.objects.values()
        accesos = PuntoAcceso.objects.values()

        acceso = [acceso for acceso in accesos if empresas if acceso["geolocalizacion"]==data["geolocalizacion"] and acceso["nombre_empresa"]==data["nombre_empresa"]]
        print("Acceso",acceso)
        if len(acceso) != 0:
            return Response({"Message":"Direccion registrado"})

        if serializer_acceso.is_valid():

            empresa = [empresa for empresa in empresas if empresa["nombre_empresa_p"]==data["nombre_empresa"]]
            if empresa == []:
                return Response({"Message":"Empresa no esta registrada"})
            serializer_acceso.save()
        return Response(serializer_acceso.data)


class ReadPuntosAccesoViews(APIView):
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
        
        p_accesos = PuntoAcceso.objects.values()

        acceso_final = []
        for p_acceso in p_accesos:
            geo = p_acceso["geolocalizacion"]
            p_acceso.pop("geolocalizacion")
            p_acceso["geolocalizacion"] = ast.literal_eval(geo)
            acceso_final.append(p_acceso)

        return Response(acceso_final)

class ReadPuntoAccesoIndividualViews(APIView):
    def get(self, request, company):

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

        p_accesos = PuntoAcceso.objects.values()

        #list_acceso = [acceso for acceso in p_accesos if acceso["nombre_empresa"]==company]

        acceso_final = []
        for p_acceso in p_accesos:
            if p_acceso["nombre_empresa"]==company:
                geo = p_acceso["geolocalizacion"]
                p_acceso.pop("geolocalizacion")
                p_acceso["geolocalizacion"] = ast.literal_eval(geo)
                acceso_final.append(p_acceso)

        if acceso_final == []:
            return Response({"message": "no hay datos sobre la empresa"})

        return Response(acceso_final)

class UpdatePuntoAccesoViews(APIView):
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

        check_e = check_email(data["email"])

        if check_e == 1:
            pass
        elif check_e == 0:
            return Response({"message": "Correo invalido"})

        direccion_finalList = []
        direccion = data["direccion"].split()
        #direccion = re.split("[#-]", direccion)
        direccion = [re.split("[#-]", direc) for direc in direccion]
        for d in range(len(direccion)):
            dirc = direccion[d]
            extraer = [di for di in dirc if di != '']
            if extraer != []:
                if d == 3 or d == 2:
                    direccion_finalList.append(',')
                for ex in range(len(extraer)):
                    concatenar = extraer[ex]
                    direccion_finalList.append(concatenar)
        direccion_finalList.append(",")
        direccion_finalList.append(data["ciudad"])
        
        direccion_final = " ".join(direccion_finalList)
        
        geo1 = {}
        try:
            geo = geolocalizacion(direccion_final)
        except:
            return Response({"Message": "No existe direccion"})
        geo1["lat"] = geo["lat"]
        geo1["lon"] = geo["lon"]
        geo1["info"] = geo["display_name"]

        data["geolocalizacion"] = f"{geo1}"
        
        p_accesos = PuntoAcceso.objects.values()
        p_acceso1 = [acceso for acceso in p_accesos if acceso["nombre_empresa"]==data["nombre_empresa"]]

        list_acceso = [[clave, valor] for clave, valor in data.items()]
        try:
            list_acceso_query = [[clave, valor] for clave, valor in p_acceso1[0].items()]
        except:
            return Response({"message":"No existe empresa"})

        dict_response = {}
        for l in range(len(list_acceso_query)-1):
            listP = list_acceso[l]
            listQ = list_acceso_query[l]
            if (listP[1]==listQ[1]) or (listP[1]==""):
                dict_response[listQ[0]] = listQ[1]
            elif (listP[1]!=listQ[1]):
                dict_response[listP[0]] = listP[1]
        
        
        serializer = PuntoAccesoSerializer(data=data)
        if serializer.is_valid():
            print(serializer.validated_data.get("geolocalizacion"))
            puntos_accesos = PuntoAcceso.objects.values()


            for p_acceso in puntos_accesos:
                list_val_dir = [pa for pa in puntos_accesos if pa["geolocalizacion"]==serializer.validated_data.get("geolocalizacion")]
                if list_val_dir == []:
                    return Response({"Message": "No existen direccion con esta empresa"})
                if  p_acceso["geolocalizacion"]==serializer.validated_data.get("geolocalizacion"):
                    id_old = p_acceso["id_access"]
                    print("Id_old", id_old)
            serializer.save()
                    #PuntoAcceso.objects.filter(geolocalizacion=geo_delete).first().delete()
                    
            #serializer.save()
            try:
                PuntoAcceso.objects.filter(id_access=id_old).first().delete()
            except:
                return Response(serializer.data)
        return Response(serializer.data)

class DeletePuntoAccesoView(APIView):
    def post(self, request):

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

        data = request.data


        direccion_finalList = []    
        direccion = data["direccion"].split()
        #direccion = re.split("[#-]", direccion)
        direccion = [re.split("[#-]", direc) for direc in direccion]
        for d in range(len(direccion)):
            dirc = direccion[d]
            extraer = [di for di in dirc if di != '']
            if extraer != []:
                if d == 3 or d == 2:
                    direccion_finalList.append(',')
                for ex in range(len(extraer)):
                    concatenar = extraer[ex]
                    direccion_finalList.append(concatenar)
        direccion_finalList.append(",")
        direccion_finalList.append(data["ciudad"])
        
        direccion_final = " ".join(direccion_finalList)
        
        geo1 = {}
        try:
            geo = geolocalizacion(direccion_final)
        except:
            return Response({"Message": "No existe direccion"})
        geo1["lat"] = geo["lat"]
        geo1["lon"] = geo["lon"]
        geo1["info"] = geo["display_name"]

        data["geolocalizacion"] = f"{geo1}"


        p_accesos = PuntoAcceso.objects.values()
        p_acceso1 = [acceso["id_access"] for acceso in p_accesos if acceso["nombre_empresa"]==data["nombre_empresa"] and acceso["geolocalizacion"]==data["geolocalizacion"]]
        print(p_acceso1)
        try:
            PuntoAcceso.objects.filter(id_access=int(p_acceso1[0])).first().delete()
        except:
            return Response({"message": "Empresa no coincide con la direccio o no esta registada"})
        #print(list_empresa)

        response_query = {"mesaage": "Eliminada correctamete"}


        return Response(response_query)





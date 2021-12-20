import re
import pandas as pd
import validators
from urllib.parse import urlparse
from geopy.geocoders import Nominatim, GoogleV3
import geocoder
from functools import partial
from datetime import datetime


###Validador Url
def is_url(url):
    try:
        resultado = urlparse(url)
        return all([resultado.scheme, resultado.netloc])
    except ValueError:
        return False

##Validador correo #####
def check_email(email):
    regex_my = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if(re.search(regex_my, email)):
        return 1
    else:
        return 0

#Geolocalizacion
def geolocalizacion(direccion):
    #geolocator = Nominatim(user_agent="proyecto")
    geolocator = GoogleV3()
    location, (lat, long) = geolocator.geocode(direccion)
    return print(location, lat, long)

def geolocalizacion1(direccion):
    result = geocoder.google(direccion)
    return result.latlng

now = datetime.now()
 #Fecha
#temp = pd.Timestamp(now.date())
#print(temp.dayofweek, temp.day_name())#Dia de la semana
#geolocalizacion("calle 152b # 72 - 91 Bogota")



# prueba tecnica
Prueba tecnica USEIT.co

#### Para poder correr el proyecto, primero se tiene que instalar el entorno, nos dirigimos al CMD o se prefiere anaconda promp. 

```html
python -m venv proyecto1 python
```
```html
proyecto1\Scripts\activate.bat
```

#### Luego de instalar el entorno, debemos dirigirnos a la carpeta donde quedó descargado el proyecto mediante CMD y continuamos con el proceso de instalacion de las librerias para el proyecto.



```html
pip install django==3.1.7
```
```html
pip install djangorestframework==3.12.2
```
```html
pip install PyJWT==1.7.1
```
```html
pip install django-cors-headers
```
```html
pip install validators
```
```html
pip install geopy
```
```html
pip install pandas
```
```html
pip install requests
```
#### Ya instalada las librerías necesarias para el proyecto, entonces nos dirigimos a la carpeta “proyecto_final” mediante consola, luego de eso escribimos la siguiente línea de código para poder correr el ´proyecto. 
```html
python manage.py runserver
```

## Test proyecto
Dado que no pude terminar el Front-End, se harán las pruebas en Postman de las APIs; dentro del respositorio podrán encontrar un llamado **my_project.postman_collection**, donde podrán importar esta colleccion de peticiones junto a las urls(APIs) y JSON generados en su aplicación Postman.

Antes de empezar la explicación les compartiré dos correos electrónicos con sus respectivas contraseñas para que puedan visualizar que algunos puntos requeridos en la prueba técnica están correctamente ejecutados, estos correos serán eliminados luego de recibir la respuesta de la prueba técnica.

##### El primer correo es para poder registrar la empresa:

Email:

dueno.empresa123@gmail.com

Password:

dueno.empresa123_@

##### El segundo correo es para poder registrar un usuario “empleado” en la pagina:

Email:

usuarioempresa02@gmail.com

Password:

dueno.empresa123_@

## CRUD Administrador o propietario

#### La primera petición (POST):

Con esta petición se podrá registrar el usuario administrador.

http://127.0.0.1:8002/api/registerPropietario

#### JSON(ejemplo):
```html
{
    "cedula_propietario": 23456,
    "nombre_propietario": "Wilfredo Vargas",
    "email_propietario": "dueno.empresa123@gmail.com",
    "usuario_propietario": "wilfredo123",
    "password": "12345",
    "telefono_propietario": "+57 3502233456"
}
```

#### Segunda petición (POST):

Con esta petición se podrá hacer el login del usuario administrador.

http://127.0.0.1:8002/api/loginPropietario

#### JSON(ejemplo):
```html
{
    "email": "dueno.empresa123@gmail.com",
    "password": "12345"
}
```

#### Tercera petición (GET):

Con esta petición se podrá hacer un filtrado para poder visualizar el usuario administrador logeado en ese momento.

http://127.0.0.1:8002/api/readPropietario

#### Cuarta petición (POST):

Con esta petición se podrá hacer la actualización de los campos del usuario administrador.

http://127.0.0.1:8002/api/uploadPropietario

#### JSON(ejemplo):
```html
{
    "cedula_propietario": 2278,
    "nombre_propietario": "Wilfredo",
    "email_propietario": "dueno.empresa123@gmail.com",
    "usuario_propietario": "Wilfredo",
    "password": "12345",
    "telefono_propietario": "+57 3502233456"
}
```
#### Quinta petición (GET):

Con esta petición se podrá hacer la visualizar todos los usuarios resgistrados usuario administrador.

http://127.0.0.1:8002/api/readPropietarioAll


#### Sexta petición (GET):

Con esta petición se podrá cerrar la sesión del usuario administrador.

http://127.0.0.1:8002/api/logoutPropietario

#### Septima petición (GET):

Con esta petición se podrá eliminar usuario administrador.

http://127.0.0.1:8002/api/eliminarProietario

## CRUD Empresa propietaria

#### La primera petición (POST):

Con esta petición se podrá registrar la empresa propietaria.

http://127.0.0.1:8002/api/registerEmpresa

#### JSON(ejemplo):
```html
{
    "nit_p": 1212,
    "nombre_empresa_p": "Mufu",
    "nombre_comercial_p": "Mufu SAS",
    "telefono_p": "+57 3445566",
    "direccion_p": "calle 152b # 72",
    "user_admin_p": "Wilfredo Vargas",
    "email_p": "dueno.empresa123@gmail.com",
    "web_p": "http://www.mufu.com",
    "pais_p": "Colombia",
    "estado_p": "Activo",
    "ciudad_p": "Bogota DC" 
}
```

#### Segunda petición (GET):

Con esta petición se podrá visualizar todos las empresas registradas.

http://127.0.0.1:8002/api/readAllEmpresa

#### Tercera petición (GET):

Con esta petición se podrá hacer un filtrado para poder visualizar el la empresa registrada según el Nit.

http://127.0.0.1:8002/api/readIndEmpresa/1212

**1212** -> Este numero que se visualiza al final de petición, es el numero del Nit de la empresa(propietaria).

#### Cuarta petición (GET):

Con esta petición se podrá eliminar la empresa registrada según el Nit.

http://127.0.0.1:8002/api/deleteEmpresa/1212

**1212** -> Este numero que se visualiza al final de petición, es el numero del Nit de la empresa(propietaria)

#### Quinta petición (POST):

Con esta petición se podrá hacer la actualización de los campos de la empresa(propietaria).

http://127.0.0.1:8002/api/uploadEmpresa

```html
{
    "nit_p": 1212,
    "nombre_empresa_p": "Mufu",
    "nombre_comercial_p": "Mufu SAS",
    "telefono_p": "+57 3445566",
    "direccion_p": "calle 152b # 72",
    "user_admin_p": "Wilfredo Vargas",
    "email_p": "dueno.empresa123@gmail.com",
    "web_p": "http://www.mufu.com",
    "pais_p": "Colombia",
    "estado_p": "Activo",
    "ciudad_p": "Bogota DC" 
}
```

## CRUD Empresa Cliente

#### La primera petición (POST):

Con esta petición se podrá registrar la empresa cliente.

http://127.0.0.1:8002/api/registerCliente

#### JSON(ejemplo):
```html
{
    "nit_c": 4567,
    "nombre_empresa_c": "bolsas",
    "nombre_comercial_c": "bolsas S.A.S",
    "telefono_c": "+57 3445566",
    "direccion_c": "calle 73B # 72-91",
    "user_admin_c": "Stiven Mora",
    "email_c": "bolsas@gmail.com",
    "web_c": "http://www.bolsas.com",
    "pais_c": "Colombia",
    "estado_c": "Cundinamarca",
    "ciudad_c": "Bogota DC" 
}
```

#### Segunda petición (GET):

Con esta petición se podrá visualizar todos las empresas (Cliente) registradas.

http://127.0.0.1:8002/api/readAllCliente

#### Tercera petición (GET):

Con esta petición se podrá hacer un filtrado para poder visualizar el la empresa (cliente) registrada según el Nit.

http://127.0.0.1:8002/api/readIndCliente/4567

**4567** -> Este numero que se visualiza al final de petición, es el numero del Nit de la empresa(Cliente).

#### Cuarta petición (POST):

Con esta petición se podrá hacer la actualización de los campos de la empresa(Cliente).

http://127.0.0.1:8002/api/uploadCliente

```html
{
    "nit_c": 4567,
    "nombre_empresa_c": "bolsas",
    "nombre_comercial_c": "bolsas A",
    "telefono_c": "+57 3445566",
    "direccion_c": "calle 73B # 72-91",
    "user_admin_c": "Stiven Mora",
    "email_c": "bolsas@gmail.com",
    "web_c": "http://www.bolsas.com",
    "pais_c": "Colombia",
    "estado_c": "Cundinamarca",
    "ciudad_c": "Bogota DC" 
}
```
#### Quinta petición (GET):

Con esta petición se podrá eliminar la empresa (Cliente) registrada según el Nit.

http://127.0.0.1:8002/api/deleteCliente/4567

**4567** -> Este numero que se visualiza al final de petición, es el numero del Nit de la empresa(Cliente).

## Puntos de acceso


#### La primera petición (POST):

Con esta petición se podrá registrar punto de acceso.

http://127.0.0.1:8002/api/registerCliente

#### JSON(ejemplo):
```html
{
    "nombre_empresa": "Mufu",
    "direccion": "calle 152b # 92",
    "ciudad": "Bogota",
    "email": "usuarioempresa02@gmail.com",
    "estado": "Activo"
}
```

#### Segunda petición (GET):

Con esta petición se podrá visualizar todos los puntos de acceso resgitrados.

http://127.0.0.1:8002/api/readAllPuntoAcceso

#### Tercera petición (GET):

Con esta petición se podrá hacer un filtrado para poder visualizar el punto de acceso segundo el nombre de la empresa registrada.

http://127.0.0.1:8002/api/readPuntoAcessoInd/Mufu

**Mufu** -> Este numero que se visualiza al final de petición, es el numero del Nit de la empresa(Cliente).

#### Cuarta petición (POST):

Con esta petición se podrá hacer la actualización de los campos de los puntos de acceso.

http://127.0.0.1:8002/api/updatePuntoAcceso

#### JSON(ejemplo):

```html
{
    "nit_c": 4567,
    "nombre_empresa_c": "bolsas",
    "nombre_comercial_c": "bolsas A",
    "telefono_c": "+57 3445566",
    "direccion_c": "calle 73B # 72-91",
    "user_admin_c": "Stiven Mora",
    "email_c": "bolsas@gmail.com",
    "web_c": "http://www.bolsas.com",
    "pais_c": "Colombia",
    "estado_c": "Cundinamarca",
    "ciudad_c": "Bogota DC" 
}
```

#### Quinta petición (POST):

Con esta petición se podrá eliminar el punto registrado según el nombre de la empresa, direccion y ciudad.

http://127.0.0.1:8002/api/deletePuntoAccesoView


#### JSON(ejemplo):

```html
{
    "nombre_empresa": "Mufu",
    "direccion": "calle 152b # 99",
    "ciudad": "Bogota"
}
```

## CRUD Usuarios Empleados de empresas propietarias

#### La primera petición (POST):

Con esta petición se podrá registrar el usuario empleado.

http://127.0.0.1:8002/api/registerEmpleado

#### JSON(ejemplo):
```html
{
    "cedula_empleado": 11223344,
    "nombre_empleado": "Diego Cabrera",
    "email_empleado": "usuarioempresa02@gmail.com",
    "usuario_empleado": "diego13",
    "password": "12345",
    "telefono_empleado": "+57 3502233456",
    "empresa": "Mufu"
}
```

#### Segunda petición (POST):

Con esta petición se enviara un link con una imagen al correo del usuario empleado para poder validar su información.

http://127.0.0.1:8002/api/sendEmailValidacionEmpleado

#### JSON(ejemplo):

```html
{
    "email": "usuarioempresa02@gmail.com"
}
```
#### Imagen enviada al correo del usuario empleado:

![Figura 1](proyecto_final/usuario_empleado/templates/send.jpg)

#### Tercera petición (GET):

Al mometo que el usuario empleado le de click en la imagen lo llevara a un link en una pestaña aparte haciendo su validacion por correo electronico.

http://127.0.0.1:8002/api/validacionEmpleado/diego13

#### JSON(ejemplo):

```html
{
    "email": "usuarioempresa02@gmail.com"
}
```

#### Cuarta petición (POST):

Con esta petición se podra logear el usuario empleado.

http://127.0.0.1:8002/api/validacionEmpleado/diego13

#### JSON(ejemplo):

```html
{
    "email_empleado": "usuarioempresa02@gmail.com",
    "password": "12345"
}
```

**Al momento de que el usuario empleado dijite mal su password, se envaiará al correo electronico al jefe del empleado, haciendo le saber cuantas veces a intentado ingresar y el dia y la hora**

#### Quinta petición (POST):

Con esta peticion el usuario podrá actualizar algunos campos.

http://127.0.0.1:8002/api/uploadEmpleado

#### JSON(ejemplo):

```html
{
    "cedula_empleado": 11223344,
    "nombre_empleado": "Diego Pineda",
    "email_empleado": "diegoc@gmail.com",
    "usuario_empleado": "diego13",
    "password": "12345",
    "telefono_empleado": "+57 3502233456",
    "empresa": "Hewtech"
}
```

#### Quinta petición (GET):

Eliminar cuenta de usuario empleado segun su cedula .

http://127.0.0.1:8002/api/deleteEmpleado/11223344

**11223344** -> Cedulá usuario

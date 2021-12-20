import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.template.loader import render_to_string
from proyecto_final import settings
import os
import requests
from datetime import datetime
NOW_ABS_FILEPATH = os.path.dirname(os.path.abspath(__file__))
def send_email(email_send, url):
        

    #try:
        mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        print(mailServer.ehlo())
        mailServer.starttls()
        print(mailServer)
        mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        mensaje = MIMEMultipart()
        mensaje["From"] = settings.EMAIL_HOST
        mensaje["To"] = email_send
        mensaje["subject"] = "Correo Validacion"
        
        print("path", NOW_ABS_FILEPATH)

        content = render_to_string(f"{NOW_ABS_FILEPATH}\\templates\\send.html", {"url": url})
        mensaje.attach(MIMEText(content, 'html'))
        print("conectado..")


        mailServer.sendmail(settings.EMAIL_HOST_USER,
                            email_send,
                            mensaje.as_string())
        print("Correo enviado correctamente")
        return {"Message": "Correo enviado correctamente"}

def send_email_error(email_send, user, empresa):
        now = datetime.now()
    #try:
        mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        print(mailServer.ehlo())
        mailServer.starttls()
        print(mailServer)
        mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        mensaje = MIMEText(f"""El usuario {user} intento ingresar a la empresa {empresa} el dia {now.date()} a las {now.hour}:{now.minute}""")
        mensaje["From"] = settings.EMAIL_HOST
        mensaje["To"] = email_send
        mensaje["subject"] = "Usuario intento acceder"
        
        print("path", NOW_ABS_FILEPATH)

        print("conectado..")


        mailServer.sendmail(settings.EMAIL_HOST_USER,
                            email_send,
                            mensaje.as_string())
        print("Correo enviado correctamente")
        return {"Message": "Correo enviado correctamente"}
    #except Exception as ex:
        #return ex    

# Create your tests here.

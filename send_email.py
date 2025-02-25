import smtplib, ssl
import os


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "rafael.gutierrez4666@alumnos.udg.mx"
    password = "srlssvmbxshpdldi"

    receiver = "ARTURO.CRUZ.1210@ibm.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)

# Script propiedad de Pedro Jesús del Moral


import keyring



import getpass
import sys
import os
from datetime import datetime
import ftplib
import tarfile
import logging
import keyring


if len(sys.argv)==2:
	
	if sys.argv[1] == "--correo":
		print("Establecer la contraseña del correo de forma segura")
		contracorreo = getpass.getpass("Contraseña del correo: ")

		# Guardar contraseña
		keyring.set_password("contracorreo", "contracorreo", contracorreo)
	elif sys.argv[1] == "--ftp":
		print("Establecer la contraseña del servidor FTP de forma segura")
		contraftp = getpass.getpass("Contraseña del FTP: ")
		# Guardar contraseña
		keyring.set_password("contraftp", "contraftp", contraftp)
	elif sys.argv[1] == "--zip":
		print("Establecer la contraseña para el comprimido")
		contrazip = getpass.getpass("Contraseña del comprimido: ")

		# Guardar contraseña
		keyring.set_password("contrazip", "contrazip", contrazip)

	
	elif sys.argv[1] == "--todo":
		contracorreo = getpass.getpass("Contraseña del correo: ")
		contraftp = getpass.getpass("Contraseña del FTP: ")
		contrazip = getpass.getpass("Contraseña del comprimido: ")
		# Guardar contraseña
		keyring.set_password("contracorreo", "contracorreo", contracorreo)
		keyring.set_password("contraftp", "contraftp", contraftp)
		keyring.set_password("contrazip", "contrazip", contrazip)
	else:
		print("Parametro incorrecto, solo se acepta --correo, --ftp --todo")
	
contrasenacorreo = keyring.get_password("correobackup", "usuariocorreo")
contrasenaftp = keyring.get_password("usuarioftp", "usuarioftp")
contrazip = keyring.get_password("contrazip", "contrazip")
	
# Obtener la fecha actual
fecha = datetime.now()
fechaestringeada = fecha.strftime("%Y%m%d")


    
    
    
    
    
    
    
# Comprimir directorio public_html
nombre_archivo = "servidor_web.tar.gz"
comprimir = tarfile.open(nombre_archivo, "w:gz")
comprimir.add("/home/usuario/apache")
comprimir.close()


import zipfile
# importing module
import pyminizip

# input file path
inpt = "/home/usuario/"+nombre_archivo

# prefix path
pre = "/home/usuario/"

# output zip file path
oupt = "/home/usuario/backup"+fechaestringeada+".zip"

# set password value
password = contrazip

# compress level
com_lvl = 5

# compressing file
pyminizip.compress(inpt, pre, oupt, password, com_lvl)


nombrecomprimido="backup"+fechaestringeada+".zip"




# Conectarse al servidor FTP
ftp = ftplib.FTP()
ftp.connect("127.0.0.1",21)
ftp.sendcmd('USER alberto_virtual')
ftp.sendcmd('PASS '+contrasenaftp)
# Subir archivo comprimido al servidor
archivoasubir = open(nombrecomprimido, "rb")
ftp.storbinary("STOR " + nombrecomprimido, archivoasubir)
archivoasubir.close()







# Eliminar archivo local
#os.remove(zip_file_name)

# Borrar la copia de seguridad más antigua si hay más de 10 en el servidor
lista_archivos = ftp.nlst()
lista_archivos.sort()
if len(lista_archivos) > 10:
    ftp.delete(lista_archivos[0])
ftp.quit()


from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib #importar el modulo de protocolos de correo
sender='pejemofe@pejemofe.es' #Dirección del remitente
receiver='pejemofe@gmail.com' #Dirección del destinatario
password= contrasenacorreo #Contraseña de la cuenta del remitente
#Detalles de conexión al servidor de correo
smtp_server=smtplib.SMTP("smtp.ionos.es",587)
smtp_server.ehlo() #Iniciando la conexión por IMAP
smtp_server.starttls() #Configurando la conexión con encriptación TLS
smtp_server.ehlo() #Iniciando de nuevo la conexión con encriptación TLS
smtp_server.login(sender,password) #Logeándose en el servidor de correo
#Mensaje que se enviará
mensaje ='''
La copia de seguridad de la web se ha realizado correctamente
'''
#Añadiendo contenido en cabeceras de Asunto, remitente y destinatario
mensajeconcabeceras = MIMEMultipart()
mensajeconcabeceras["Subject"] = "Copia seguridad OK"
mensajeconcabeceras["From"] = sender
mensajeconcabeceras["To"] = receiver
mensajeconcabeceras.attach(MIMEText(mensaje))


#Enviar el correo
smtp_server.sendmail(sender,receiver,mensajeconcabeceras.as_string())
smtp_server.quit()#Cerrando el servicio de correo


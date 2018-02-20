from __future__ import print_function
import imutils
import cv2
import numpy
import os
import RPi.GPIO as GPIO
import time
from cv2 import *
import picamera
from ftplib import FTP
import time


#Activacion del GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor

#Seteo del FTP a utilizar
def envio(imagen):
	# Nombre del fichero origen
	fileName=imagen
	# Ubicacion del fichero origen
	routeOrigin="/home/pi/"
	# Ubicacion donde colocar el fichero destino
	routeDestination="/fotos/"
	try:
		# abrimos la conexion con el servidor
		ftp=FTP("ftp.epizy.com","epiz_21504314","matrix94")
		# Canviamos de directorio
		ftp.cwd(routeDestination)
		# Subimos el archivo
		ftp.storbinary("STOR %s" % fileName,open("%s%s" % (routeOrigin,fileName)))
        
		ftp.quit()
	except Exception,e:
		print (e)

try:
	os.remove("image15b.jpg")
	print ("iniciando 1")
except Exception, e:
	print ("iniciando2")

#Toma de imagen a comparar

camera = picamera.PiCamera()
camera.capture('image15b.jpg')

image = cv2.imread("image15b.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gris = cv2.GaussianBlur(image, (21, 21), 0)




while True:
	i=GPIO.input(11)
	if i==0:                 #When output from motion sensor is LOW
		print ("No intruders",i)
		time.sleep(0.01)

	elif i==1:              
		print ("Intruder detected",i)
		imagen='image16b.jpg'
		camera.capture('image16b.jpg')
		image2 = cv2.imread("image16b.jpg")
		gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (21, 21), 0)
		gray3 = gray -gris
	
		resta = cv2.absdiff(gray, gris)
		resultado = resta.flatten()
		comparative = numpy.sum(resultado)
		print (comparative)
		if comparative<50052095:
			print("Falsa Alarma")
		else:
			envio(imagen)
			cv2.imwrite('image'+time.strftime("%c")+'.jpg', image2)
			cv2.imwrite('diferencia'+time.strftime("%c")+'.jpg', gray3)
		os.remove("image16b.jpg")
		#os.remove("delete2.jpg")
		time.sleep(0.01)

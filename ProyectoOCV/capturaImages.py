#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 17:03:14 2018

@author: root
"""
import time
import os
import picamera
import paramiko
import numpy as np
import cv2

# Conecta con el servidor sftp al servidor awaresystems.cl
host = "awaresystems.cl"                    
port = 22222
transport = paramiko.Transport((host, port))

transport.connect(username = "cesar", password = "cesar1234")

sftp = paramiko.SFTPClient.from_transport(transport)

height=480*3
width=640*3


# Activa y configura la cámara de la Raspberry
camera = picamera.PiCamera()
camera.resolution = (width, height)

# Sube la foto tomada por la cámara al servidor
def envio():
    path =  '/home/cesar/ProyectoOCV/temp/' 
    localpath = './temp/image.jpg' 
    sftp.put(localpath, path)

    sftp.close()
    transport.close()
    return 'Imagen subida'


# Elimina la imagen en caso de que estuviera
try:
	os.remove("temp/image.jpg")
	print ("iniciando 1")
except Exception:
	print ("iniciando2")

# Toma fotografías cada 1 segundo
while (True):
    output = np.empty((height,  width, 3,), dtype=np.uint8)
    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="rgb")
    cv2.imwrite('./temp/image.jpg', output)
    print(envio())
    #os.remove("temporal/image.jpg")
    time.sleep(1)

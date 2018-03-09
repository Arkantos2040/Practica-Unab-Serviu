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
import sys
import numpy as np
import cv2


host = "awaresystems.cl"                    #hard-coded
port = 22222
transport = paramiko.Transport((host, port))

transport.connect(username = "cesar", password = "cesar1234")

sftp = paramiko.SFTPClient.from_transport(transport)

height=480*3
width=640*3



camera = picamera.PiCamera()
camera.resolution = (width, height)
def envio():
    path =  '/home/cesar/recogn/temp/'  #hard-coded
    localpath = './temporal/image.jpg' 
    sftp.put(localpath, path)

    sftp.close()
    transport.close()
    return 'Imagen subida'



try:
	os.remove("temporal/image.jpg")
	print ("iniciando 1")
except Exception:
	print ("iniciando2")

while (True):
    output = np.empty((height,  width, 3,), dtype=np.uint8)
    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="rgb")
    cv2.imwrite('./temporal/image.jpg', output)
    print(envio())
    #os.remove("temporal/image.jpg")
    time.sleep(1)

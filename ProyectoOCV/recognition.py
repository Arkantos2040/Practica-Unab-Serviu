#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 00:04:24 2018

@author: root
"""
from __future__ import print_function
import datetime
import face_recognition
import time
import cv2
import urllib2
#import cookielib
#import urllib


try:
    registro = open("registro.txt", "r")
    registro.close()
except Exception:
    registro = open("registro.txt", "w")
    registro.close()
image1 = face_recognition.load_image_file("registrados/Sebastián_Carreño.png")
image2 = face_recognition.load_image_file("registrados/César_Cheuque.png")
image3 = face_recognition.load_image_file("registrados/Ignacio_Zamorano.png")
image4 = face_recognition.load_image_file("registrados/Juan_Calderon.jpg")
image5 = face_recognition.load_image_file("registrados/Karen_Alaluf.jpg")
image6 = face_recognition.load_image_file("registrados/Mauricio_Poblete.jpg")
image7 = face_recognition.load_image_file("registrados/Giannina_Costa.jpg")
image8 = face_recognition.load_image_file("registrados/Romina_Torres.jpg")
image9 = face_recognition.load_image_file("registrados/Paulo_Negrete.png")
list_persons = ("Sebastián_Carreño", "César_Cheuque", "Ignacio_Zamorano", "Juan_Calderon", "Karen_Alaluf","Mauricio_Poblete",
                "Giannina_Costa", "Romina_Torres", "Paulo_Negrete")

image1_face_encoding = face_recognition.face_encodings(image1)[0]
image2_face_encoding = face_recognition.face_encodings(image2)[0]
image3_face_encoding = face_recognition.face_encodings(image3)[0]
image4_face_encoding = face_recognition.face_encodings(image4)[0]
image5_face_encoding = face_recognition.face_encodings(image5)[0]
image6_face_encoding = face_recognition.face_encodings(image6)[0]
image7_face_encoding = face_recognition.face_encodings(image7)[0]
image8_face_encoding = face_recognition.face_encodings(image8)[0]
image9_face_encoding = face_recognition.face_encodings(image9)[0]
dict_recon={}


image_face_encoding = (image1_face_encoding, image2_face_encoding, image3_face_encoding, 
                       image4_face_encoding, image5_face_encoding, image6_face_encoding,
                       image7_face_encoding, image8_face_encoding, image9_face_encoding)

image_face_tupla = tuple(image_face_encoding)
j=0
for images_face in image_face_encoding:
    dict_recon[tuple(images_face)]=list_persons[j]
    j=j+1

# Initialize some variables
face_locations = []
face_encodings = []
def recog(dictionary, encoded, taked, image):
    for imagesEncoded in encoded:

        
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces([imagesEncoded], taked)
        
        if match[0]:
            name = dictionary[tuple(imagesEncoded)]

            return name
    name = "Persona Desconocida"
    cv2.imwrite('./saved/'+name+"_"+time.strftime("%c")+'.jpg', image)
    f = open('registro.txt','a')
    f.write('\n' + "Registro de: "+name+"    Fecha: "+time.strftime("%c"))
    f.close()
    site= "http://ignacio.awaresystems.cl/insertarAlertaAdulto.php?intentoAlerta=1&estadoAlerta=1&tipoAlerta=Persona_Desconocida&Usuario_id_usuario=12"
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                       'Accept-Encoding': 'none',
                       'Accept-Language': 'en-US,en;q=0.8',
                       'Connection': 'keep-alive'}
    req = urllib2.Request(site, headers=hdr)
    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        print (e.code)

    content = page.read()
    print (content)
    return name
        
    
    
    
while True:
    try:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        image = face_recognition.load_image_file('./temp/image.jpg')
    
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(image)
    
        print("Se encuentran {} rostros en la imagen.".format(len(face_locations)), now)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        # Loop over each face found in the frame to see if it's someone we know.
    
            
        for face_encoding in face_encodings:
            print("Registrado : {}!".format(recog(dict_recon, image_face_encoding,face_encoding, image)), now)
    except Exception:
        print ("No se detecta nada")
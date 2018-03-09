#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 11:33:46 2018

@author: César Cheuque Cerda
"""

from __future__ import print_function
import datetime
import face_recognition
import time
import cv2
import urllib3
import os
import glob
import datetime

# Creación del archivo de registro
try:
    registro = open("registro.txt", "r")
    registro.close()
except Exception:
    registro = open("registro.txt", "w")
    registro.close()
    
#Variable para la ruta al directorio
path = './registrados'
 
#Lista vacia para incluir los ficheros
lstFiles = []
list_persons =()
 
#Lista con todos los ficheros del directorio:
lstDir = os.walk(path)   #os.walk()Lista directorios y ficheros
 
 
#Crea una lista de los ficheros jpg que existen en el directorio y los incluye a la lista.
images_faces_encoding = ()

for root, dirs, files in lstDir:
    for fichero in files:
        #print (fichero)
        (nombreFichero, extension) = os.path.splitext(fichero)
        if(extension == ".jpg" or extension== ".png"):
            image = face_recognition.load_image_file("registrados/"+fichero)
            image_face_encoding = face_recognition.face_encodings(image)[0]
            images_faces_encoding = images_faces_encoding + (image_face_encoding,)
            list_persons = list_persons  +  (nombreFichero, )
            lstFiles.append(nombreFichero+extension)



dict_recon={}


image_face_tupla = tuple(images_faces_encoding)
j=0
for images_face in images_faces_encoding:
    dict_recon[tuple(images_face)]=list_persons[j]
    j=j+1

# Initialize some variables
face_locations = []
face_encodings = []
def recog(dictionary, encoded, taked, image):
    for imagesEncoded in encoded:

        
        # See if the face is a match for the known face(s)
        match = face_recognition.api.compare_faces([imagesEncoded], taked, tolerance= 0.5)
        
        if match[0]:
            name = dictionary[tuple(imagesEncoded)]
            try:
                os.mkdir("/home/cesar/www/fotos/"+name)
            except Exception:
                pass
            path2 = '/home/cesar/www/fotos/'+name+"/"
            nameFile= path2+name+"_"+now+'.jpg'
            print(nameFile)
            cv2.imwrite(nameFile, image)
            latestFile = datetime.datetime.fromtimestamp(os.path.getmtime(nameFile))
            f = open('registro.txt','a')
            f.write('\n' + "Registro de: "+name+"    Fecha: "+time.strftime("%c"))
            f.close()
            lstDir2 = os.walk(path2)
            if (len(glob.glob(path2+'/*.jpg'))>4):
                print(len(glob.glob(path2+'/*.jpg')))
                for root, directory, files in lstDir2:
                    for archivo in files:
                        curpath = os.path.join(path2, archivo)
                        file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(curpath))
                        if (datetime.datetime.now() - latestFile <= datetime.datetime.now() - file_modified):
                            latestFile = file_modified
                            OldestFile = curpath
                    os.remove(OldestFile)

                            
                            
                        
                        
                    
                

            return name
    name = "Persona Desconocida"
    cv2.imwrite('/home/cesar/www/fotos/Desconocidos/'+name+"_"+now+'.jpg', image)
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
    req = urllib3.Request(site, headers=hdr)
    try:
        page = urllib3.urlopen(req)
    except urllib3.HTTPError as e:
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
            print("Registrado : {}!".format(recog(dict_recon, images_faces_encoding,face_encoding, image)), now)
    except Exception:
        print ("No se detecta nada")
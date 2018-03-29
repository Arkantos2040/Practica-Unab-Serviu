#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 11:33:46 2018

@author: César Cheuque Cerda

Se recomienda leer cada comentario para que el programa funcione OK
"""
#carga de librerías
from __future__ import print_function
import datetime
import face_recognition
import time
import cv2
import os
#import os.path as ruta
import glob
#import urllib2 #para trabajar con python2 descomentar esta línea y comentar la siguiente
import urllib.request as urllib2 #para trabajar con python3 descomentar esta línea y comentar la anterior

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

#Se crea una tupla codificadas para la detección de rostros de todos los archivos .jpg .png en el directorio registrados
#además crea una tupla con los nombres de los archivos sin extensión de los mismos
for root, dirs, files in lstDir:
    for fichero in files:
        #print (fichero)
        (nombreFichero, extension) = os.path.splitext(fichero)
        if(extension == ".jpg" or extension== ".png"):
            image = face_recognition.load_image_file("./registrados/"+fichero)
            image_face_encoding = face_recognition.face_encodings(image)[0]
            images_faces_encoding = images_faces_encoding + (image_face_encoding, )
            list_persons = list_persons  +  (nombreFichero, )
            lstFiles.append(nombreFichero+extension)


dict_recon={}

# Define ruta de dónde se guardarán las fotos que el sistema guarde tanto de las personas reconocidas como de desconocidos

pathO="/home/cesar/www/fotos/"
#pathO="./borrar/"

# Se crea un diccionario de las tuplas ya creadas donde las imágenes codificadas serán las llaves y los nombres serán el valor asociado a las llaves
j=0
for images_face in images_faces_encoding:
    dict_recon[tuple(images_face)]=list_persons[j]
    j=j+1

#Inicia listas necesarias
face_locations = []
face_encodings = []

#Función de reconocimiento facial
def recog(dictionary, encoded, taked, image):
    for imagesEncoded in encoded:
        
        # Evalúa si el rostro de la imagen tomada "taken" corresponde a uno de las personas en la tupla creada
        match = face_recognition.compare_faces([imagesEncoded], taked, tolerance= 0.54)
        if match[0]:
 
            name = dictionary[tuple(imagesEncoded)]
            try:

                os.mkdir(pathO+name)
            except Exception:

                pass
            # Guarda un registro de cada persona encontrada y la foto de esta en una carpeta separada a cada persona
            path2 = pathO+name+"/"
            nameFile= path2+name+"_foto1.jpg"
            try:
                latestFile = datetime.datetime.fromtimestamp(os.path.getmtime(nameFile))
            except Exception:
                pass
            lstDir2 = os.walk(path2)
            
            # Elimina una imagen de la persona cada vez que se llega a 5 por persona
            if(len(glob.glob(path2+'/*.jpg'))==0):
                print(len(glob.glob(path2+'/*.jpg')))
                nameFile= path2+name+"_foto1.jpg"
                cv2.imwrite(nameFile, image)
            elif(len(glob.glob(path2+'/*.jpg'))==1):
                nameFile= path2+name+"_foto2.jpg"
                cv2.imwrite(nameFile, image)
            elif(len(glob.glob(path2+'/*.jpg'))==2):
                nameFile= path2+name+"_foto3.jpg"
                cv2.imwrite(nameFile, image)
            elif(len(glob.glob(path2+'/*.jpg'))==3):
                nameFile= path2+name+"_foto4.jpg"
                cv2.imwrite(nameFile, image)
            else:
                #print(len(glob.glob(path2+'/*.jpg')))
                for root, directory, files in lstDir2:
                    for archivo in files:
                        curpath = os.path.join(path2, archivo)
                        file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(curpath))
                        if (datetime.datetime.now() - latestFile <= datetime.datetime.now() - file_modified):
                            latestFile = file_modified
                            OldestFile = curpath
                    os.remove(OldestFile)
                    nameFile= OldestFile
                    cv2.imwrite(nameFile, image)
            return name
    # Si la persona en cuestion no es reconocida, genera una alerta en la aplicación, guarda en la base de datos y guarda la imagen de esta.
    name = "Persona Desconocida"
    cv2.imwrite(pathO+name+"_"+now+'.jpg', image)
    f = open('registro.txt','a')
    f.write('\n' + "Registro de: "+name+"    Fecha: "+time.strftime("%c"))
    f.close()
    
    site= "http://ignacio.awaresystems.cl/insertarAlertaAdulto.php?intentoAlerta=1&estadoAlerta=1&tipoAlerta=Persona_Desconocida&Usuario_id_usuario=12"
    alerta ="http://ignacio.awaresystems.cl/notificacion.php?mensaje=Persona_desconocida"
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                       'Accept-Encoding': 'none',
                       'Accept-Language': 'en-US,en;q=0.8',
                       'Connection': 'keep-alive'}
    resp= urllib2.Request(alerta, headers=hdr)

    req = urllib2.Request(site, headers=hdr)

    try:
        page2=urllib2.urlopen(resp)

        page = urllib2.urlopen(req)
    except urllib2.HTTPError as e:

        print (e.code)

    content = page.read()
    content2=page2.read()
    print (content2)
    print (content)
    
    return name
            
    
    
# Ejecución del Programa    
while True:
    try:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Recupera la imagen guardada en la carpeta temporal
        image = face_recognition.load_image_file('./temp/image1.jpg')
        image2 = face_recognition.load_image_file('./temp/image2.jpg')
        # Identifica como tal todos los rostros que están presentes la imagen recuperada
        face_locations = face_recognition.face_locations(image)
        face_locations2 = face_recognition.face_locations(image2)
        print("Se encuentran {} rostros en la imagen. Camara 1.".format(len(face_locations)), now)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        print("Se encuentran {} rostros en la imagen. Camara 2.".format(len(face_locations2)), now)
        face_encodings2 = face_recognition.face_encodings(image2, face_locations2)
        # Crea un loop de reconocimiento por cada rostro identificado como tal de la imagen recuperada 
            
        for face_encoding in face_encodings:
            
            print("Registrado : {}!".format(recog(dict_recon, images_faces_encoding,face_encoding, image)), now)
        for face_encoding in face_encodings2:
            
            print("Registrado : {}!".format(recog(dict_recon, images_faces_encoding,face_encoding, image2)), now)
    except Exception:
        print("nada que detectar")
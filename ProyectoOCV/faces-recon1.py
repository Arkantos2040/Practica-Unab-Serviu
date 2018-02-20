#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 19:21:58 2018

@author: Cesar Cheuque
"""


import picamera
import numpy as np
import cv2
import datetime
import face_recognition
import time

height=240
width=320



camera = picamera.PiCamera()
camera.resolution = (width, height)
#output = np.empty((380 * 307 * 3), dtype=np.uint8)



# Load a sample picture and learn how to recognize it.
print("Loading known face image(s)")
image1 = face_recognition.load_image_file("registrados/seba.png")
image2 = face_recognition.load_image_file("registrados/cesar.png")
image3 = face_recognition.load_image_file("registrados/Ignacio.png")
image4 = face_recognition.load_image_file("registrados/juan-calderon.jpg")
image5 = face_recognition.load_image_file("registrados/Karen_Alaluf.jpg")
image6 = face_recognition.load_image_file("registrados/pao.png")
image7 = face_recognition.load_image_file("registrados/giannina-costa.jpg")
image8 = face_recognition.load_image_file("registrados/Romina_Torres.jpg")
image9 = face_recognition.load_image_file("registrados/Paulo_Negrete.png")
list_persons = ("seba", "cesar", "ignacio", "juan_calderon", "Karen Alaluf","pao",
                "gianina costa", "Romina Torres", "paulo negrete")

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
            cv2.imwrite('./saved/image'+time.strftime("%c")+'.jpg', image)
            return name
    name = "Persona Desconocida"
    return name
        
    
    
    
while True:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Capturing image.")
    output = np.empty((height,  width, 3,), dtype=np.uint8)
    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="rgb")

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(output)

    print("Se encuentran {} rostros en la imagen.".format(len(face_locations)), now)
    face_encodings = face_recognition.face_encodings(output, face_locations)
    
    # Loop over each face found in the frame to see if it's someone we know.

        
    for face_encoding in face_encodings:
        



            print("Registrado : {}!".format(recog(dict_recon, image_face_encoding,face_encoding, output)), now)

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 13:23:49 2018

@author: root
"""
import cv2
import time


vcap = cv2.VideoCapture("rtsp://10.40.3.13:8554/x")
time.sleep(2)
frames =1
while True:
        ret, frame = vcap.read()
        print ("test")
        cv2.imshow('frame',frame)
        frames =frames + 1
        print (frames)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quit")
            break

vcap.release()
cv2.destroyWindow(vcap)
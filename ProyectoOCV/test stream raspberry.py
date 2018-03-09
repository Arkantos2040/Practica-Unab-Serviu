#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 13:23:49 2018

@author: root
"""
import cv2
import time


vcap = cv2.VideoCapture("rtsp://192.168.1.150:8554/x")
time.sleep(2)
while(1):
    ret, frame = vcap.read()
    cv2.imshow('VIDEO', frame)
    cv2.waitKey(1)
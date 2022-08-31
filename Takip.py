# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 13:51:02 2022

@author: DHAMLE2
"""
import cv2
import numpy as np
from collections import deque
import time
import serial.tools.list_ports
import math
from time import sleep
buffer_size = 16
pts = deque(maxlen = buffer_size)
mavi_say=0
sarı_say = 0
kalibre_genislik = 5.0 # cm
kalibre_uzunluk  = 7.5 # cm
#%%
cap = cv2.VideoCapture(0)
cap.set(3,960)
cap.set(4,480)
#%%
frame_width_cm = 23.5
after_comma = 2
frame_width_px = cap.get(4)
frame_height_px = cap.get(3)
px_in_cm = frame_width_cm / frame_width_px
print("frame: wh",frame_width_px,frame_height_px)
print("px in cm:",px_in_cm)
#%%
while True:
    success, imgOriginal = cap.read()
    if success: 
        blurred = cv2.GaussianBlur(imgOriginal, (11,11), 0) 
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        hsv += 25
        mask = cv2.inRange(hsv, (20,  155,  0), (52, 255, 255))
        mask = cv2.erode(mask, None, iterations = 2)
        mask = cv2.dilate(mask, None, iterations = 2)
        (contours,_) = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        center = None
        if len(contours) > 0:
            c = max(contours, key = cv2.contourArea)     
            rect = cv2.minAreaRect(c)     
            ((x,y), (width,height), rotation) = rect  
            (x,y,width,height,rotation)=(np.round(x),np.round(y),np.round(width),np.round(height),np.round(rotation))    
            coord_center = ( int(frame_height_px / 2), int(frame_width_px/2) )
            cv2.circle(imgOriginal,coord_center , 5, (255,0,255),-1)
            x_cm = x * px_in_cm
            y_cm = y * px_in_cm
       #     print("center cm x:",x_cm,"y:",y_cm)
            coord_x_px = x - float(frame_height_px) / 2.0
            coord_y_px =  float(frame_width_px) / 2.0 - y
            coord_x_cm = round( coord_x_px * px_in_cm, after_comma )
            coord_y_cm = round( coord_y_px * px_in_cm, after_comma )
            print("coord_px x:",coord_x_cm,"y:",coord_y_cm)
            s = "x: {}, y: {}, width: {}, height: {}, rotation: {}".format(np.round(x),np.round(y),np.round(width),np.round(height),np.round(rotation))
           # print(s)        
            #result = "x: {},\n,y: {}".format(np.coord_x_cm,np.coord_y_cm)          
            box = cv2.boxPoints(rect)
            box = np.int64(box)
            M = cv2.moments(c)
            center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
            cv2.drawContours(imgOriginal, [box], 0, (0,255,255),2)
            cv2.circle(imgOriginal, center, 5, (255,0,255),-1)
            cv2.putText(imgOriginal, s, (25,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 2)
        pts.appendleft(center)
        cv2.line(imgOriginal, (930, 0), (930, 560), (0, 0, 0), 5)                  
        for i in range(1, len(pts)):  
            if pts[i-1] is None or pts[i] is None: continue
            cv2.line(imgOriginal, pts[i-1], pts[i],(0,255,0),3)   
        cv2.imshow("Orijinal Tespit",imgOriginal)          
    if cv2.waitKey(1) & 0xFF == ord("q"): 
        break 
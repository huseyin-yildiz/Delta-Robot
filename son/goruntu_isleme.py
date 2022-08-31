#%% imports
from son.haberlesme import CMD_MAVI, CMD_SARI
from collections import deque
import cv2
import numpy as np
import time



#%% Kamera Ayarlari
buffer_size = 16
pts = deque(maxlen = buffer_size)
mavi_say=0
sarı_say = 0
cap = cv2.VideoCapture(0)
cap.set(3,960)
cap.set(4,480)
#%% Kamera - Obje ayarlari   !!! dikkat !!! Bunlari ayarlamadan calistirirsaniz hatali sonuclar elde edil.
frame_width_cm = 19.5
after_comma = 2
frame_width_px = cap.get(4)
frame_height_px = cap.get(3)
px_in_cm = frame_width_cm / frame_width_px
print("frame: wh",frame_width_px,frame_height_px)
print("px in cm:",px_in_cm)





def renk_say(renk):
    global mavi_say
    global sarı_say
    global x
    global y
    while True:
        videoCapture()    
        if renk == CMD_MAVI:
            if x>10  :
                if y<10 :
                    mavi_say = mavi_say  + 1
                    print(mavi_say)
                    time.sleep(1)
        elif renk == CMD_SARI:
            if x>10  :                            
                if y<10 :
                    sarı_say = sarı_say  + 1
                    print(sarı_say)
                    return sarı_say
                    time.sleep(1) 
        
        if renk == "q": 
            break     




        #%%
def renk_ayırma():
   print ("renk ayirma")




#%%
def renk_takip():
    global coord_x_cm
    global coord_y_cm
    #Basla()
    while True:
        videoCapture() 
        print("coord_px x:",coord_x_cm,"y:",coord_y_cm)
        





        
def videoCapture():
    success, imgOriginal = cap.read()
    if success: 
        imgOriginal = imgOriginal[0:960,275:565] 
        blurred = cv2.GaussianBlur(imgOriginal, (11,11), 0)      
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, Renk_Lower(read),Renk_Upper(read)) 
        mask = cv2.erode(mask, None, iterations = 2)
        mask = cv2.dilate(mask, None, iterations = 2) 
        (contours,_) = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        center = None
        if len(contours) > 0:
            c = max(contours, key = cv2.contourArea)  
            rect = cv2.minAreaRect(c)
            ((x,y), (width,height), rotation) = rect
            s = "x: {}, y: {}, width: {}, height: {}, rotation: {}".format(np.round(x),np.round(y),np.round(width),np.round(height),np.round(rotation))
            print(s)  
            (x,y,width,height,rotation)=(np.round(x),np.round(y),np.round(width),np.round(height),np.round(rotation))
            x = np.round(x)
            y = np.round(y)                
            box = cv2.boxPoints(rect)
            box = np.int64(box)
            M = cv2.moments(c)
            center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))            
            cv2.drawContours(imgOriginal, [box], 0, (0,255,255),2)
            cv2.circle(imgOriginal, center, 5, (255,0,255),-1)
            cv2.putText(imgOriginal, s, (25,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 2) 
            #coord_center = ( int(frame_height_px / 2), int(frame_width_px/2) )
            coord_center = (145, int(frame_width_px/2) )
            x_cm = x * px_in_cm
            y_cm = y * px_in_cm
            coord_x_px = x - 145
            coord_y_px =  float(frame_width_px) / 2.0 - y
            coord_x_cm = round( coord_x_px * px_in_cm, after_comma )
            coord_y_cm = round( coord_y_px * px_in_cm, after_comma )
            center_point=[coord_x_cm,coord_y_cm]
        pts.appendleft(center)
        cv2.line(imgOriginal, (930, 0), (930, 560), (0, 0, 0), 5)                  
        for i in range(1, len(pts)):
            if pts[i-1] is None or pts[i] is None: continue
            cv2.line(imgOriginal, pts[i-1], pts[i],(0,255,0),3) # 
        cv2.imshow("Orijinal Tespit",imgOriginal)






def Renk_Lower(a):
    if a == "Mavi":
        blueLower = (85,  97,  0)
        return blueLower
    elif a=="Sarı":
        blueLower = (20,  127,  0)
        return blueLower
    else:
        Okuyucu()
        Renk_Lower(read)    
def Renk_Upper(b):       
    if b == "Mavi":
        blueUpper = (178,  255,  255)
        return blueUpper
    elif b=="Sarı":
        blueUpper = (52, 255, 255)
        return blueUpper
    else:
        Okuyucu()
        Renk_Upper(read)

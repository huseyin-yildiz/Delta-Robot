
'''
Kodların Toplandığı dosya
'''
import cv2
import numpy as np
from collections import deque
import time
import serial.tools.list_ports
import math
from time import sleep
import RPi.GPIO as GPIO

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
#%%    
def renk_say(read):
    global mavi_say
    global sarı_say
    global x
    global y
    while True:
        videoCapture()    
        if read=="Mavi":
            if x>10  :
                if y<10 :
                    mavi_say = mavi_say  + 1
                    print(mavi_say)
                    time.sleep(1)
        elif read == "Sarı":
            if x>10  :                            
                if y<10 :
                    sarı_say = sarı_say  + 1
                    print(sarı_say)
                    return sarı_say
                    time.sleep(1) 
        
        if read == "q": 
            break     
#%%
def renk_ayırma(d):
    #Basla()
    while True:
        Okuyucu()
        success, imgOriginal = cap.read()
        if success:     
            blurred = cv2.GaussianBlur(imgOriginal, (11,11), 0) 
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            hsv += 25
            cv2.imshow("HSV Image",hsv)
           
            mask = cv2.inRange(hsv, Renk_Lower(read),Renk_Upper(read))
            cv2.imshow("mask Image",mask)
            mask = cv2.erode(mask, None, iterations = 2)
            mask = cv2.dilate(mask, None, iterations = 2)
            cv2.imshow("Mask + erozyon ve genisleme",mask)
            (contours,_) = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                c = max(contours, key = cv2.contourArea)
                rect = cv2.minAreaRect(c)
                ((x,y), (width,height), rotation) = rect
                s = "x: {}, y: {}, width: {}, height: {}, rotation: {}".format(np.round(x),np.round(y),np.round(width),np.round(height),np.round(rotation))
                print(s)
                (x,y,width,height,rotation)=(np.round(x),np.round(y),np.round(width),np.round(height),np.round(rotation))
                x = np.round(x)
                y = np.round(y)
        Okuyucu()
        if read == "q": 
           # Dur()
            read=""
            break
    xp = x*0,264   # xp  ve yp gerçek koordinat sistemindeki x ve y olucak 
    yp = y*0,264 
    Ub = 346.600
    Ua = 20.450
    Wb = 142.5
    Wa = 142.5
    L = 390
    d1 = Ub * math.cos(30)
    d2 = Ua * math.cos(30)
    d4 = Ua * math.sin(30)
    d3 = Ub * math.sin(30)
    zp = 50
    q1 = zp + math.sqrt((L ^ 2) - ((-d1 + xp + d2) ^ 2) - ((d3 + yp - d4) ^ 2)) #® ?? z ?? 
    q2 = zp + math.sqrt((L ^ 2) - ((d1 + xp - d2) ^ 2) - ((d3 + yp - d4) ^ 2))
    q3 = zp + math.sqrt((L ^ 2) - ((xp) ^ 2) - ((Ub + yp) ^ 2))
    R=  2*math.pi*2.5*0.1125/360
    step = (q1 / R)
    step1 = (q2 / R)
    step2 = (q3 / R)
    MODE = (14,15,18)
    RESOLUTION = {"1/32": (1,0,1)}
    GPIO.output(MODE,RESOLUTION["1/32"])
    DIR = 20
    CW = 1
    SPR = step
    SPR1 = step1  
    SPR2 = step2
    STEP = 21
    STEP1 = 16
    STEP2 = 19 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR,GPIO.OUT)
    GPIO.setup(STEP,GPIO.OUT)
    GPIO.setup(STEP1,GPIO.OUT)
    GPIO.setup(STEP2,GPIO.OUT)
    GPIO.output(DIR,CW)
    step_count = SPR
    step_count = SPR1
    step_count = SPR2
    delay=0.0208
    for z in range(step_count):
        GPIO.output(STEP,GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP,GPIO.LOW)
        sleep(delay)
    sleep(0.5)
    for z in range(step_count):
        GPIO.output(STEP1,GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP1,GPIO.LOW)
        sleep(delay)
    sleep(0.5)
    for z in range(step_count):
        GPIO.output(STEP2,GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP2,GPIO.LOW)
        sleep(delay)
    sleep(5)
    q11 = zp + math.sqrt((L ^ 2) - ((-d1 + xp + d2) ^ 2) - ((d3 + yp - d4) ^ 2)) 
    q11 = q11-q1
    q22 = zp + math.sqrt((L ^ 2) - ((d1 + xp - d2) ^ 2) - ((d3 + yp - d4) ^ 2))
    q22 = q22-q2
    q33 = zp + math.sqrt((L ^ 2) - ((xp) ^ 2) - ((Ub + yp) ^ 2))
    q33 = q33-q1
    step = (q11 / R)
    step1 = (q11 / R)
    step2 = (q22 / R)
    SPR = step
    SPR1 = step1  
    SPR2 = step2
    step_count = SPR
    step_count1 = SPR1
    step_count2 = SPR2
    if q11<0:
        CW = 0
        abs(q11)
        GPIO.output(DIR,CW)
        for z in range(step_count):
            GPIO.output(STEP,GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP,GPIO.LOW)
            sleep(delay)
        sleep(0.5) 
    elif q11>0:
        CW = 1
        GPIO.output(DIR,CW)
        for z in range(step_count):
            GPIO.output(STEP,GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP,GPIO.LOW)
            sleep(delay)
        sleep(0.5) 
    else:
        pass
    if q22<0:
        CW = 0
        abs(q22)
        GPIO.output(DIR,CW)
        for z in range(step_count1):
            GPIO.output(STEP,GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP,GPIO.LOW)
            sleep(delay)
        sleep(0.5) 
    elif q22>0:
        CW = 1
        GPIO.output(DIR,CW)
        for z in range(step_count1):
            GPIO.output(STEP,GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP,GPIO.LOW)
            sleep(delay)
        sleep(0.5) 
    else:
        pass
    if q33<0:
        CW = 0
        abs(q33) 
        GPIO.output(DIR,CW)
        for z in range(step_count2):
            GPIO.output(STEP,GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP,GPIO.LOW)
            sleep(delay)
        sleep(0.5) 
    elif q22>0:
        CW = 1
        GPIO.output(DIR,CW)
        for z in range(step_count2):
            GPIO.output(STEP,GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP,GPIO.LOW)
            sleep(delay)
        sleep(0.5) 
    else:
        pass
    videoCapture()
    '''
def Foto():
    success, imgOriginal = cap.read()
    if success:  
        blurred = cv2.GaussianBlur(imgOriginal, (11,11), 0) 
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        cv2.imshow("HSV Image",hsv)
        read = ser.redline()
        mask = cv2.inRange(hsv, Renk_Lower(read),Renk_Upper(read))
        cv2.imshow("mask Image",mask)
        mask = cv2.erode(mask, None, iterations = 2)
        mask = cv2.dilate(mask, None, iterations = 2)
        cv2.imshow("Mask + erozyon ve genisleme",mask)  
        (contours,_) = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            c = max(contours, key = cv2.contourArea)
            rect = cv2.minAreaRect(c)    
            ((x,y), (width,height), rotation) = rect
            s = "x: {}, y: {}, width: {}, height: {}, rotation: {}".format(np.round(x),np.round(y),np.round(width),np.round(height),np.round(rotation))
            print(s)  
            (x,y,width,height,rotation)=(np.round(x),np.round(y),np.round(width),np.round(height),np.round(rotation))
            x = np.round(x)
            y = np.round(y)
    '''
#%%
def renk_takip(e):
    global read
    global coord_x_cm
    global coord_y_cm
    #Basla()
    while True:
        videoCapture() 
        print("coord_px x:",coord_x_cm,"y:",coord_y_cm)
        
        
        if read == "q": 
            break   
#%%
'''
def Dur():
    GPIO.output(input1,GPIO.LOW)
    sleep(0.5)
def Basla():
    GPIO.output(input1,GPIO.HIGHT)
    '''
#%%
def Okuyucu():
    while 1:       
        read_1 = ser.redline()
        if read_1 ==b'':
            read = "1"
            break
        elif read_1 ==b'':
            read="2"
            break
        elif read_1 == b'':
            read="3"
            break
        elif read_1 == b'':
            read="Sarı"
            break
        elif read_1 == b'':
            read="Mavi"
            break
        elif read_1 == b'':
            read="q"
            break
        else:
            pass
#%%
buffer_size = 16
pts = deque(maxlen = buffer_size)
mavi_say=0
sarı_say = 0
cap = cv2.VideoCapture(0)
cap.set(3,960)
cap.set(4,480)
#%%
frame_width_cm = 19.5
after_comma = 2
frame_width_px = cap.get(4)
frame_height_px = cap.get(3)
px_in_cm = frame_width_cm / frame_width_px
print("frame: wh",frame_width_px,frame_height_px)
print("px in cm:",px_in_cm)
#%%
ser = serial.Serial(port='/dev/ttyUSB0',
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1)

# Motor çalıştırma
input1 = 24
en = 18 
GPIO.setmode(GPIO.BCM)
GPIO.setup(input1,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(input1,GPIO.HIGHT)
p=GPIO.PWM(en,1000)
p.start(50)

while True: 
    if read == b'':
        Okuyucu()
    else:
        if read=="1":
            renk_say(read)
        elif read =="2":
            renk_takip(read)
        elif read =="3":
            renk_ayırma(read)
        else:
            Okuyucu()
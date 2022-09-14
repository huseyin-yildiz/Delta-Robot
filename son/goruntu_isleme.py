#%% imports
from haberlesme import write_cmd
from collections import deque
import cv2
import numpy as np
import time
from motor import *
from motor import motor_calistir
import math
from threading import Thread
from konum_takip import *
from tracker import *




tracker = EuclideanDistTracker()
passed_ids = deque(maxlen=200)
count_area_size = 10
count_border_down = real_length / 5 - count_area_size / 2
count_border_up   = count_border_down + count_area_size

count = 0

real_middle = (int(real_length / 2), int( real_width / 2 ) ) 


### 3 Step motorun pin ayarları
DIR = 20 # Yönünü belirten pinler
DIR_1 = 26
DIR_2 = 13 ####

CW = 1
# Step mtorlardaki adım sayılarının kontrol edileceği pinler
STEP_pin = 21
STEP1_pin = 16
STEP2_pin = 19 
### Pinlerin kurlumu
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR,GPIO.OUT)
GPIO.setup(DIR_1,GPIO.OUT)
GPIO.setup(DIR_2,GPIO.OUT)
GPIO.setup(STEP_pin,GPIO.OUT)
GPIO.setup(STEP1_pin,GPIO.OUT)
GPIO.setup(STEP2_pin,GPIO.OUT)
###
###



COLOR_YELLOW = 0
COLOR_BLUE = 1
COLOR_RED = 2


BGR_YELLOW = (0,255,255)
BGR_RED = (0,0,255)
BGR_BLUE = (255,0,0)


buffer_size = 16
pts = deque(maxlen = buffer_size)
cap = cv2.VideoCapture(0)
cap.set(3,960)
cap.set(4,544)


corner_points = [(0, 24), (804, 192), (0, 199), (804, 13)]

# global count
# count = 0



# #%% Kamera Ayarlari
# def setup_cam():
#     global buffer_size = 16
#     global pts = deque(maxlen = buffer_size)
#     global cap = cv2.VideoCapture(0)
#     cap.set(3,960)S
#     cap.set(4,480)
# 
# frame_width_cm = 19.5
# after_comma = 2
# frame_width_px = cap.get(4)
# frame_height_px = cap.get(3)
# px_in_cm = 46 / 960 # 51.8 ?
# 
# coord_y_cm = 0
# 


# print("frame: wh",frame_width_px,frame_height_px)
# print("px in cm:",px_in_cm)

# 0 noktasındayken q1,q2ve q3 lerin aldeğı değerler
step_1 = [213.83]
step_2 = [213.83]
step_3 = [213.83]
#####

def get_img():
    
    success, img = cap.read()
    if success:

        img = img[135:345,75:880] 
        img = perspective_transform(img,corner_points)
        
        blurred = cv2.GaussianBlur(img, (11,11), 0)      
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)        
        gama_corrected_hsv = gama_hsv(hsv)
        
        return img,gama_corrected_hsv
        
        # detect_objects(img)
        # renk_say(img,gama_corrected_hsv,COLOR_YELLOW)
#         renk_takip(img,gama_corrected_hsv,COLOR_YELLOW)
#         
#         cv2.imshow("tst",img)
#         if cv2.waitKey(1) & 0xFF == ord("q"): 
#             break
#         
        

def renk_say(serial,color):
  
    global count 
    img,gama_corrected_hsv = get_img()
    
    hulls = None
    draw_color = None
    
    
    if(color == COLOR_YELLOW):
        hulls = color_filter(gama_corrected_hsv, yellow_down, yellow_up, yellow_erode, yellow_dilate)
        draw_color = BGR_YELLOW
        
    elif(color == COLOR_BLUE):
        hulls = color_filter(gama_corrected_hsv, blue_down, blue_up, blue_erode, blue_dilate)
        draw_color = BGR_BLUE
        
    elif(color == COLOR_RED):    
        hulls = color_filter(gama_corrected_hsv, red_down, red_up, red_erode, red_dilate)
        draw_color = BGR_RED
    else:
       return 
        
        
    detections = []
    for hull in hulls:
        # Calculate area and remove small elements
        area = cv2.contourArea(hull)
        if area > 100:
            #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(hull)
            detections.append([x, y, w, h])

    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        print("id",box_id)
        x, y, w, h, id = box_id
        cv2.putText(img, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(img, (x, y), (x + w, y + h), draw_color, 3)

        if(x > count_border_down and x < count_border_up and (id not in passed_ids) ):
            passed_ids.append(id)
            count += 1
            
    cv2.putText(img, str(count), (30,30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    cv2.imshow("tst",img)
    command = 't6.txt="'+str(count)+'"' 
    write_cmd(serial,command)

    

# Kinematik denklemlerdeki sabit değerler
Ub = 346.600
Ua = 20.450
Wb = 142.5
Wa = 142.5
L = 390
d1 = Ub * math.cos(30)
d2 = Ua * math.cos(30)
d4 = Ua * math.sin(30)
d3 = Ub * math.sin(30)  
###


def renk_ayirma(serial,renk):
    motor_calistir()
    
    
    img,gama_corrected_hsv = get_img()
    
        
    red_hulls = color_filter(gama_corrected_hsv, red_down, red_up, red_erode, red_dilate)
    yellow_hulls = color_filter(gama_corrected_hsv, yellow_down, yellow_up, yellow_erode, yellow_dilate)
    blue_hulls = color_filter(gama_corrected_hsv, blue_down, blue_up, blue_erode, blue_dilate)
    
    draw_contour(img, red_hulls, (0,0,255) )
    draw_contour(img, yellow_hulls, (0,255,255) )
    draw_contour(img, blue_hulls, (255,0,0) )
      
    

    #%
    # belli nir noktada konveyör bandı durdurulması
    if (coord_x_cm):
        if coord_x_cm < 4:     
            i = 0
            motor_durdur()
            # bir işlem 2 adımdan oluşucağı ve adımlar arasındaki veriler deişceği için döngü kuruldu.
            while (i < 2):
                xp = [0,0] 
                                #ikinci indeks dışardan sabit değer girilicek(kutu koordinatları)
                yp = [0,5]# ilk değer video capturedeki merkezin koordinatlarından gelicek
                            # ikinci indeks dışardan sabit değer girilicek(kutu koordinatları)
                zp = [70,30]# İlk değer sabit değer olucak
                            # ikinci indeks dışardan sabit değer girilicek(kutu koordinatları)
                ### nextion ekranına aktarmak için yazılan kodlar
                command = 't8.txt="'+str(xp[i])+'"' 
                write_cmd(command)
                time.sleep(0.005)
                
                command = 't9.txt="'+str(yp[i])+'"' 
                write_cmd(command)
                time.sleep(0.005)
                
                command = 't10.txt="'+str(zp[i])+'"' 
                write_cmd(command)
                time.sleep(0.005)
                ###
                # Kinematik denklemler mm cinsinden olduğu için alınan koordinatların mm dönüştürülmesi
                xp = [0*10,0*10] 
                yp = [0*10,5*10] 
                zp = [70*10,10*10]
               
                
                # Step motorların bir adımının ne kadar yol aldığı
                R =  (2*math.pi*5)*(0.1125/360)
                
                # Kinematik denklemler
                q1 = zp[i] + (math.sqrt((pow(L , 2) - pow((-d1 + xp[i] + d2) , 2) - pow((d3 + yp[i] - d4) , 2))) )
                step_1.append(q1) # konumlar depolandı
                q2 = zp[i] + (math.sqrt((pow(L , 2) - pow((d1 + xp[i] - d2) , 2) - pow((d3 + yp[i] - d4) , 2))))
                step_2.append(q2)
                q3 = zp[i] + (math.sqrt((pow(L , 2) - pow((Ub + yp[i] - Ua) , 2)) -  pow((xp[i]) , 2)))
                step_3.append(q3)
             
                # 2. bulunan konumdan 1. bulunan konum çıkartılarak 2.bulunan komua gitmesi için gerekli olan ölçütler
                q1 = step_1[-1]-step_2[-2]
                q2 = step_2[-1]-step_2[-2]
                q3 = step_3[-1]-step_2[-2]
                # Step motorların kaç adım atıcağını hesaplar
                step = (q1 / R)
                step1 = (q2  / R)
                step2 = (q3 / R) 
                # eksili değerse  sayının mutlak değeri alınır ve cw(dönüş yönü) fonksiyon için değiştirilir 
                step_count = abs(step)
                step_count_1 = abs(step1)
                step_count_2 = abs(step2)
                
                delay=0.0208
                
                # 3 motorda aynı anda çalıştırır
                z1 = Thread(target=step_motor_1)
                z2 = Thread(target=step_motor_2)
                z3 = Thread(target=step_motor_3)
                
                
                
                z1.start()
                z2.start()
                z3.start()

                z1.join()
                z2.join()
                z3.join()
                
                i = i + 1

def renk_takip(serial,color):
#     global coord_x_cm
#     global coord_y_cm
#     global ser
#     global stop
        
    img,gama_corrected_hsv = get_img()
    
    x=0
    y=0
    
    
    if(color == COLOR_YELLOW):
        hulls = color_filter(gama_corrected_hsv, yellow_down, yellow_up, yellow_erode, yellow_dilate)
        centers = draw_contour(img, hulls, (0,255,255) )

    elif(color == COLOR_RED):
        hulls = color_filter(gama_corrected_hsv, red_down, red_up, red_erode, red_dilate)
        centers = draw_contour(img, hulls, (0,0,255) )
    
    elif(color == COLOR_BLUE):
        hulls = color_filter(gama_corrected_hsv, blue_down, blue_up, blue_erode, blue_dilate)
        centers = draw_contour(img, hulls, (255,0,0) )
    
    cx=0
    cy=0
    
    if( len(centers) ):
        x = centers[0][0]
        y = centers[0][1]
    
        cx,cy = pixelToCoord(x,y)
        print("x:",cx,"y:",cy)
    
    command = 't6.txt="'+'x:'+str(cx)+'y:'+str(cy)+'"' 
    try:
        write_cmd(serial,command)
    except:
        print("hata")
    cv2.circle(img, real_middle, 5, (255,0,255),-1)
    cv2.imshow("tst",img)
    #time.sleep(0.05)
         
         
def pixelToCoord(x,y):
    cx = x - float(real_length) / 2.0
    cy =  float(real_width) / 2.0 - y
    return cx,cy
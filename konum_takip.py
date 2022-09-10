# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 08:28:42 2022

@author: DHAMLE2
"""
import cv2
import numpy as np
from collections import deque
import math
import time

#%%

buffer_size = 16
pts = deque(maxlen = buffer_size)
cap = cv2.VideoCapture(0)
cap.set(3,960)
cap.set(4,544)


#%%



#%%
def dist(p1, p2):
    """p1 and p2 in format (x1,y1) and (x2,y2) tuples"""
    dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
    return dis



def perspective_transform(img,src):
    # pts11 = np.float32([[0, 260], [640, 260],
    #                    [0, 400], [640, 400]])
    
    dest = np.float32([[0, 0], [real_length, real_width],
                       [0, real_width], [real_length, 0]])
     
    src = np.float32(src)
    # print("pts1:",src)
    # Apply Perspective Transform Algorithm
    #matrix = cv2.getPerspectiveTransform(src, dest)
    
    matrix, status = cv2.findHomography(src, dest)
    
    result = cv2.warpPerspective(img, matrix, (real_length, real_width))
     
    # Wrap the transformed image
    cv2.imshow('frame', img) # Initial Capture
    cv2.imshow('frame1', result) # Transformed Capture
    return result





def get_bant_corners(cap):
    while(True):
        success, img = cap.read()
        if success: 
            img = img[135:345,75:880] 
            
            blurred = cv2.GaussianBlur(img, (11,11), 0)      
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            
            hull = color_filter(hsv, green_down, green_up)[0]
            bant_points = find_corners(hull)
    
        if cv2.waitKey(1) & 0xFF == ord("q"): 
            return bant_points 



       
        
def color_filter(hsv_img,hsv_down, hsv_up, erode = 2, dilate = 2):
    
    mask = None
    if(hsv_down[0] <= hsv_up[0]):
        mask = cv2.inRange(hsv_img, hsv_down, hsv_up ) #  (20,  152,  0), (52, 255, 255)) 
    else:
        print("22")
        mask = cv2.inRange(hsv_img,hsv_down,(255,255,255) ) | cv2.inRange(hsv_img,(0,hsv_down[1],0),hsv_up )
        
    mask = cv2.erode(mask, None, iterations = erode)
    mask = cv2.dilate(mask, None, iterations = dilate ) 
   
    
    cv2.imshow("Mask",mask)
    (contours,_) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hulls = list()
    for c in contours:
        # c = max(contours, key = cv2.contourArea)  
        # rect = cv2.minAreaRect(c)

        # convexHull
        hulls.append(cv2.convexHull(c))
    return hulls
        # cv2.drawContours(imgOriginal, [hull], 0, (255,0,0), 3)
        
        
        # print ( "convex hull has ",len(hull),"points")
            
        #rect = cv2.minAreaRect(hull)
        
        #((x,y), (width,height), rotation) = rect
        #s = "x: {}, y: {}, width: {}, height: {}, rotation: {}".format(np.round(x),np.round(y),np.round(width),np.round(height),np.round(rotation))
        #print(s)
        #(x,y,width,height,rotation)=(np.round(x),np.round(y),np.round(width),np.round(height),np.round(rotation))
        #x = np.round(x)
        #y = np.round(y)                
        #box = cv2.boxPoints(rect)
        #box = np.int64(box)




def find_center(hull):
    M = cv2.moments(hull)
    if(M["m00"] == 0):
        return (0,0)
    else:    
        center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))   
        #print("c:",center)
        return center
        
        
            
            
     #   pts.appendleft(center)                 
      #  for i in range(1, len(pts)):
       #     if pts[i-1] is None or pts[i] is None: continue
        #    cv2.line(imgOriginal, pts[i-1], pts[i],(0,255,0),3) # 
        
            
            
        
        #cv2.imshow("Orijinal Tespit",imgOriginal)
        
        
     



def find_corners(hull):
    center = find_center(hull)

    points = list()
    ptt = list()
    # print("h",hull[0])
    ptt.append( filter(lambda x: x[0][0] < center[0] and x[0][1] < center[1]   , hull))
    ptt.append( filter(lambda x: x[0][0] > center[0] and x[0][1] > center[1]   , hull))
    ptt.append( filter(lambda x: x[0][0] < center[0] and x[0][1] > center[1]   , hull))
    ptt.append( filter(lambda x: x[0][0] > center[0] and x[0][1] < center[1]   , hull))
    
    
    for pt in ptt:
        distance = list()
        for p in pt :                
            ctr = tuple(p[0])
            #cv2.circle(imgOriginal, ctr, 5, (255,0,255),-1)
            distance.append( (ctr,dist(ctr,center)) )
    
        distance.sort(key = lambda x: x[1],reverse=True)
        if(distance):
            #cv2.circle(imgOriginal, distance[0][0], 5, (0,0,255),-1)
            points.append(distance[0][0])
    
    return points 
   
      
      
   
    
    #cv2.drawContours(imgOriginal, [box], 0, (0,255,255),2)
    # cv2.circle(imgOriginal, center, 5, (255,0,255),-1)
    # #cv2.putText(imgOriginal, s, (25,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 2) 
    # #coord_center = ( int(frame_height_px / 2), int(frame_width_px/2) )
    # perspective_transform(imgOriginal,points)

        

def draw_contour(img,hulls, contour_color ):
    for index, hull in enumerate(hulls):
        print(index, ":",hull)
        cv2.drawContours(img, [hull], 0, contour_color, 3)
        center = find_center(hull)
        cv2.circle(img, (center[0], center[1]), 5, contour_color,-1)
        cv2.putText(img ,str(center[0]/2) +"mm "+ str(center[1]/2) +"mm" 
                        , (center[0], center[1]+20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.6, (0,0,0), 1)
        

def gammaCorrection(img, gamma):
    invGamma = 1 / gamma

    table = [((i / 255) ** invGamma) * 255 for i in range(256)]
    table = np.array(table, np.uint8)

    return cv2.LUT(img, table)


def gamaBest(img):
    # convert img to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # compute gamma = log(mid*255)/log(mean)
    mid = 0.5
    mean = np.mean(gray)
    gamma = math.log(mid*255)/math.log(mean)
    print(gamma)
    
    # do gamma correction
    img_gamma1 = np.power(img, gamma).clip(0,255).astype(np.uint8)
    return img_gamma1


def gama_hsv(hsv):

    hue, sat, val = cv2.split(hsv)
    
    # compute gamma = log(mid*255)/log(mean)
    mid = 0.5
    mean = np.mean(val)
    gamma = math.log(mid*255)/math.log(mean)
    print(gamma)
    
    # do gamma correction on value channel
    val_gamma = np.power(val, gamma).clip(0,255).astype(np.uint8)
    
    # combine new value channel with original hue and sat channels
    hsv_gamma = cv2.merge([hue, sat, val_gamma])
    img_gamma = cv2.cvtColor(hsv_gamma, cv2.COLOR_HSV2BGR)
    
    # show results
    cv2.imshow('input', hsv)
   
    cv2.imshow('after gamma', hsv_gamma)
    
    return hsv_gamma
    
    

#%% Main Program


real_length = 700 # mm
real_width  = 160  # mm

# Upper HSV:  (88, 255, 255) green
# Lower HSV:  (48, 0, 0)

green_down = (50,111,0)
green_up = (90,255,255)    


yellow_down = (20, 70, 0) 
yellow_up = (40, 255, 255)
yellow_erode = 2
yellow_dilate = 2

red_down = (165, 70, 0) 
red_up = (10, 255, 255)
red_erode = 3
red_dilate = 2

blue_down = (108, 60, 0) 
blue_up = (126, 255, 255)
blue_erode = 2
blue_dilate = 2







corner_points = get_bant_corners(cap)

prev_frame_time = 0
new_frame_time = 0


while(True):
    success, img = cap.read()
    
    if success: 
        
        img = img[135:345,75:880] 
        img = perspective_transform(img,corner_points)
        
       
        blurred = cv2.GaussianBlur(img, (11,11), 0)      
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
        gama_corrected_hsv = gama_hsv(hsv)
        
        
        red_hulls = color_filter(gama_corrected_hsv, red_down, red_up, red_erode, red_dilate)
        yellow_hulls = color_filter(gama_corrected_hsv, yellow_down, yellow_up, yellow_erode, yellow_dilate)
        blue_hulls = color_filter(gama_corrected_hsv, blue_down, blue_up, blue_erode, blue_dilate)
        
        draw_contour(img, red_hulls, (0,0,255) )
        draw_contour(img, yellow_hulls, (0,255,255) )
        draw_contour(img, blue_hulls, (255,0,0) )
    
    new_frame_time = time.time()
    fps = int( 1/(new_frame_time-prev_frame_time) )
    prev_frame_time = new_frame_time
    cv2.putText(img, str(fps) + "FPS", (7, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 255, 0), 2, cv2.LINE_AA)
        
    cv2.imshow("Orijinal Tespit",img)
    
    
    if cv2.waitKey(1) & 0xFF == ord("q"): 
        break 
    

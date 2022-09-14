#%% imports
from typing import Deque
from konum_takip import *
from tracker import *


buffer_size = 1000
pts = deque(maxlen = buffer_size)
cap = cv2.VideoCapture(0)
cap.set(3,960)
cap.set(4,544)



 
 #%% counting

        
tracker = EuclideanDistTracker()

passed_ids = deque(maxlen=200)

count_area_size = 10
count_border_down = real_length / 5 - count_area_size / 2
count_border_up   = count_border_down + count_area_size

count = 0

while(True):
    success, img = cap.read()
    
    if success: 
        
        img = img[135:345,75:880] 
        img = perspective_transform(img,corner_points)
        
       
        blurred = cv2.GaussianBlur(img, (11,11), 0)      
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
        gama_corrected_hsv = gama_hsv(hsv)
        
        
        hulls = color_filter(gama_corrected_hsv, yellow_down, yellow_up, yellow_erode, yellow_dilate)

        # draw_center_line(img,last_hulls,last_centers, hulls)   # eger yeni merkezlerden onceki box'lar icinde olan varsa merkezler birlestirilir. 

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
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

            if(x > count_border_down and x < count_border_up and (id not in passed_ids) ):
                passed_ids.append(id)
                count += 1
            cv2.putText(img, str(count), (30,30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                


    new_frame_time = time.time()
    fps = int( 1/(new_frame_time-prev_frame_time) )
    prev_frame_time = new_frame_time
    cv2.putText(img, str(fps) + "FPS", (7, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 255, 0), 2, cv2.LINE_AA)
        
    cv2.imshow("Orijinal Tespit",img)
    
    
    if cv2.waitKey(1) & 0xFF == ord("q"): 
        break 
    
# %%

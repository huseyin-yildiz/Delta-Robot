
from konum_takip import *



buffer_size = 1000
pts = deque(maxlen = buffer_size)
cap = cv2.VideoCapture(0)
cap.set(3,960)
cap.set(4,544)

#%%

last_hulls = None
last_centers = None




 
 #%%

def draw_center_line(img, last_hulls, last_centers, center):   # eger yeni merkezlerden onceki box'lar icinde olan varsa merkezler birlestirilir. 
    
    for hull in hulls:
        
        center = is_in_hulls(last_hulls,center)
    
    
    

while(True):
    success, img = cap.read()
    
    if success: 
        
        img = img[135:345,75:880] 
        img = perspective_transform(img,corner_points)
        
       
        blurred = cv2.GaussianBlur(img, (11,11), 0)      
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
        gama_corrected_hsv = gama_hsv(hsv)
        
        
        hulls = color_filter(gama_corrected_hsv, yellow_down, yellow_up, yellow_erode, yellow_dilate)
        if( len(hulls) ):
            center = draw_contour(img, hulls, (0,255,255) )
            pts.append(center)

        # draw_center_line(img,last_hulls,last_centers, hulls)   # eger yeni merkezlerden onceki box'lar icinde olan varsa merkezler birlestirilir. 



           # cv2.line(img, (930, 0), (930, 560), (0, 0, 0), 5)                  
            for point in pts :  
                #cv2.line(imgOriginal, pts[i-1], pts[i],(0,255,0),3)   
                cv2.circle(img, (point[0], point[1]), 5, (255,255,255),-1)
       

        last_hulls = hulls

    new_frame_time = time.time()
    fps = int( 1/(new_frame_time-prev_frame_time) )
    prev_frame_time = new_frame_time
    cv2.putText(img, str(fps) + "FPS", (7, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 255, 0), 2, cv2.LINE_AA)
        
    cv2.imshow("Orijinal Tespit",img)
    
    
    if cv2.waitKey(1) & 0xFF == ord("q"): 
        break 
    
# %%

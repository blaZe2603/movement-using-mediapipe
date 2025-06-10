import cv2 as cv
import numpy as np


video = cv.VideoCapture(0)


def detect_color(color,hue_tolerance = 30):
    c = np.uint8([[color]])
    hsv = cv.cvtColor(c,cv.COLOR_BGR2HSV)

    lower_range = max(hsv[0][0][0] - hue_tolerance, 0) ,100,100
    upper_range = min(hsv[0][0][0] + hue_tolerance, 179) ,255,255
    return np.array(lower_range,dtype = np.uint8 ) , np.array(upper_range,dtype = np.uint8 ) 


while True:

    _ , frame = video.read()
    
    color_to_check = [255,0,0]
    lower_range , upper_range = detect_color(color_to_check) 
    hsv_frame = cv.cvtColor(frame,cv.COLOR_BGR2HSV)

    mask = cv.inRange(hsv_frame,lower_range,upper_range)
    kernal = np.ones((5,5),dtype= np.uint8)
    mask = cv.dilate(mask,kernal)

    final = cv.bitwise_and(frame,frame,mask = mask)

    cont, hier = cv.findContours(mask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    
    if len(cont) != 0:
        for cont in cont :
            area = cv.contourArea(cont)
            if(area > 300):
                x,y,w,h = cv.boundingRect(cont)
                frame = cv.rectangle(frame, (x,y) , (x+w,y+h) , (color_to_check) , 2)
                
                
                
    cv.imshow("av",frame) 

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv.destroyAllWindows()
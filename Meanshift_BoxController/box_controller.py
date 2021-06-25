import cv2
import numpy as np
import pyautogui
import imutils
import time

def Press(key):
    pyautogui.press(key)

cap = cv2.VideoCapture(0);

#Initial FPS
start_time = time.time()
# FPS update time in seconds
display_time = 2
fc = 0
FPS = 0
########################

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame,1)
    imgH,imgW = frame.shape[0:2]
    frame = imutils.resize(frame,height=imgH, width=imgW)

    #Show FPS
    fc+=1
    TIME = time.time() - start_time

    if (TIME) >= display_time :
        FPS = fc / (TIME)
        fc = 0
        start_time = time.time()

    fps_disp = "FPS: "+str(FPS)[:5]

    # Add FPS count on frame
    image = cv2.putText(frame, fps_disp, (10, 25),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # imshow converts BGR to RGB while saving or displaying.
    #cv2.imshow('Video Stream w/ FPS', image)
    #################################################################
    
    
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lowred = np.array([160,120,120])
    highred = np.array([179,255,255])

    lowblue = np.array([75,120,120])
    highblue = np.array([130,255,255])
    
    red_mask = cv2.inRange(hsv, lowred, highred)
    blue_mask = cv2.inRange(hsv, lowblue, highblue)

    # image/frame, start_point, end_point, color, thickness
    cv2.rectangle(frame, (0,0), (imgW,100), (255,0,0),1)
    cv2.putText(frame,'UP',(int(imgW/2),int(imgH*1/16)),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3,cv2.LINE_AA)


    cv2.rectangle(frame, (0,0), (100,imgH), (255,0,0),1)
    cv2.putText(frame,'LEFT',(int(imgW*1/16),int(imgH/2)),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3,cv2.LINE_AA)

    cv2.rectangle(frame, (imgW-100,0), (imgW,imgH), (255,0,0),1)
    cv2.putText(frame,'RIGHT',(int(imgW*13/16),int(imgH/2)),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3,cv2.LINE_AA)

    cv2.rectangle(frame, (0,imgH-100), (imgW,imgH), (255,0,0),1)
    cv2.putText(frame,'DOWN',(int(imgW/2),int(imgH*15/16)),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3,cv2.LINE_AA)

    #for the red Object
    contours,hierachy=cv2.findContours(red_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    #startpoint, endpoint, color, thickness
    for cnt in contours:
        (x,y,w,h) = cv2.boundingRect(cnt)
        cv2.rectangle(frame,(x,y),(x + w, y + h),(0,255,0),2)
        if w>60 and h > 60:
            #print((x,y,w,h))   
                   
            if x > 0 and y > 0 and x < imgW and y < 100:
                Press('up') #UP
                print('RED UP',x,y,w,h)
                break     


            if x > 0 and y > 0 and x < 100 and y < imgH:
                Press('left') #LEFT
                print('RED LEFT',x,y,w,h)
                break      

            if x > imgW-100 and y > 0 and x < imgW and y < imgH:
                Press('right') #RIGHT
                print('RED RIGHT',x,y,w,h)
                break      

            if x > 0 and y > imgH-100 and x < imgW and y < imgH:
                Press('down') #DOWN
                print('RED DOWN',x,y,w,h)
                break      


    
    #for the blue Object
    contours,hierachy=cv2.findContours(blue_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    #startpoint, endpoint, color, thickness
    for cnt in contours:
        (x,y,w,h) = cv2.boundingRect(cnt)
        cv2.rectangle(frame,(x,y),(x + w, y + h),(0,255,0),2)
        #print((x,y))
        if w>60 and h > 60:
            #print((x,y,w,h))   
                   
            if x > 0 and y > 0 and x < imgW and y < 100:
                Press('up') #UP
                print('BLUE UP',x,y,w,h)
                break     


            if x > 0 and y > 0 and x < 100 and y < imgH:
                Press('left') #LEFT
                print('BLUE LEFT',x,y,w,h)
                break      

            if x > imgW-100 and y > 0 and x < imgW and y < imgH:
                Press('right') #RIGHT
                print('BLUE RIGHT',x,y,w,h)
                break      

            if x > 0 and y > imgH-100 and x < imgW and y < imgH:
                Press('down') #DOWN
                print('BLUE DOWN',x,y,w,h)
                break        
  
    
    
    cv2.imshow("frame", frame)
    # cv2.imshow("mask", mask)
    # cv2.imshow("res", res)
 
    key = cv2.waitKey(1)
    if key == 32: #press space for exi t
        break
 
cap.release()
cv2.destroyAllWindows()
import cv2
import datetime
import time 
import numpy as np
from pynput.mouse import Controller, Button

cap = cv2.VideoCapture(0)
cap.set(3, 640) #FRAME_WIDTH
cap.set(4, 400) #FRAME_HEIGHT
cap.set(10, 150) #BRIGHTNESS

m = Controller()

last_click = datetime.datetime.now()

#Initial FPS
start_time = time.time()
# FPS update time in seconds
display_time = 2
fc = 0
FPS = 0
########################

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    
    #Show FPS
    fc += 1
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

    lower_blue = np.array([75, 130, 130])
    upper_blue = np.array([125, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    cv2.imshow("mask_blue", mask_blue)

    lower_green = np.array([60, 156, 25])
    upper_green = np.array([80, 255, 121])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    cv2.imshow("mask_green", mask_green)

    _, contoursBlue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contoursBlue :
        if cv2.contourArea(c) <= 50 :
            continue
        x, y, _, _ = cv2.boundingRect(c)
        m.position = x*1920/640, y*1080/400
        print(m.position)
        cv2.drawContours(frame, contoursBlue, -1, (0, 255, 0), 3)

    _, contoursGreen, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contoursGreen :
        if cv2.contourArea(c) <= 50 :
            continue
        now = datetime.datetime.now()
        diff = now - last_click
        if diff.total_seconds() > 0.1 :
            last_click = datetime.datetime.now()
            cv2.drawContours(frame, contoursGreen, -1, (0, 255, 0), 3)
            x, y = m.position
            print("CLICK",x, y)
            m.click(Button.left, 1)
    
    cv2.imshow("Camera_Control", frame)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
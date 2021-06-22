import cv2
import numpy as np
import pyautogui
import imutils
import tkinter as tk

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

def Press(key):
    pyautogui.press(key)

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame,1)
    #frame = imutils.resize(frame,height=1600, width=800)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lowred = np.array([131,90,106])
    highred = np.array([255,255,255])

    lowblue = np.array([40,150,116])
    highblue = np.array([255,255,255])

    red_mask = cv2.inRange(hsv, lowred, highred)
    blue_mask = cv2.inRange(hsv, lowblue, highblue)

    # image/frame, start_point, end_point, color, thickness
    cv2.rectangle(frame, (0,0), (900,150), (255,0,0),1)
    cv2.putText(frame,'UP',(440,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3,cv2.LINE_AA)


    cv2.rectangle(frame, (0,160), (150,570), (255,0,0),1)
    cv2.putText(frame,'LEFT',(10,350),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3,cv2.LINE_AA)

    cv2.rectangle(frame, (750,160), (900,570), (255,0,0),1)
    cv2.putText(frame,'RIGHT',(770,350),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3,cv2.LINE_AA)

    cv2.rectangle(frame, (0,580), (900,700), (255,0,0),1)
    cv2.putText(frame,'DOWN',(440,640),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3,cv2.LINE_AA)

    #for the red Object
    contours,hierachy=cv2.findContours(red_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    #startpoint, endpoint, color, thickness
    for cnt in contours:
        (x,y,w,h) = cv2.boundingRect(cnt)
        cv2.rectangle(frame,(x,y),(x + w, y + h),(0,255,0),2)
        if w>60 and h > 60:
            #print((x,y,w,h))   
                   
            if x > 0 and y > 0 and x < 900 and y < 150:
                #Press('A') #UP
                print('RED UP',x,y,w,h)
                break     


            if x > 0 and y > 160 and x < 150 and y < 570:
                Press('B') #LEFT
                print('RED LEFT',x,y,w,h)
                break      

            if x > 750 and y > 160 and x < 900 and y < 570:
                Press('C') #RIGHT
                print('RED RIGHT',x,y,w,h)
                break      

            if x > 0 and y > 580 and x < 900 and y < 700:
                Press('D') #DOWN
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
                   
            if x > 0 and y > 0 and x < 900 and y < 150:
                #Press('A') #UP
                print('BLUE UP',x,y,w,h)
                break     


            if x > 0 and y > 160 and x < 150 and y < 570:
                Press('B') #LEFT
                print('BLUE LEFT',x,y,w,h)
                break      

            if x > 750 and y > 160 and x < 900 and y < 570:
                Press('C') #RIGHT
                print('BLUE RIGHT',x,y,w,h)
                break      

            if x > 0 and y > 580 and x < 900 and y < 700:
                Press('D') #DOWN
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
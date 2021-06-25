# Face&Smile + Fist

import numpy as np
import cv2
import pynput.mouse
import time

start_time = time.time()
# FPS update time in seconds
display_time = 2
fc = 0
FPS = 0

mouse=pynput.mouse.Controller()

# OpenCV contains many pre-trained classifiers for face, eyes, smile etc.
# All we have to do is load the required XML classifiers.
face_file = './haarcascade_frontalface_default.xml'
smile_file = './haarcascade_smile.xml'
fist_file = './fist.xml'

face_cascade = cv2.CascadeClassifier( face_file )
smile_cascade = cv2.CascadeClassifier(smile_file)
fist_cascade = cv2.CascadeClassifier(fist_file)

# Check whether the two model files are loaded successfully
if not face_cascade.empty() :
    print( face_file , "loaded successfully." )
else:
    print( "Failed to load", face_file )

if not smile_cascade.empty() :
    print( smile_file , "loaded successfully." )
else:
    print( "Failed to load", smile_file )
if not fist_cascade.empty() :
    print( fist_file , "loaded successfully." )
else:
    print( "Failed to load", fist_file )

    
camera = cv2.VideoCapture(0)
while True:
    ret,frame_bgr = camera.read()
    frame_bgr=cv2.flip(frame_bgr,1)
    
    if ret == False or frame_bgr is None:
        print("Cannot get an image from the camera.")
        continue

    frame_gray = cv2.cvtColor( frame_bgr, cv2.COLOR_BGR2GRAY )

    fists = fist_cascade.detectMultiScale(frame_gray, 1.2, 5)
    for (sx, sy, sw, sh) in fists:
            cv2.rectangle(frame_bgr, (sx, sy), ((sx + sw), (sy + sh)), (255, 0, 0), 2)
            
            # Draw circle in the center of the bounding box
            x2 = sx + int(sw/2)
            y2 = sy + int(sh/2)
            cv2.circle(frame_bgr,(x2,y2),4,(255,0,0),-1)
            # Print the centroid coordinates
            text = "x: " + str(x2) + ", y: " + str(y2)
            cv2.putText(frame_bgr, text, (x2 - 10, y2 - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            #print(text)
            
            mouse.position = (x2 , y2)
            #mid_x=(sx+sx+sw)/2
           # mid_y=(sy+sy+sh)/2
            #mouse.move(-1*7*sx,7*sy)
            
    
    # Detect face(s) in the camera image.
    faces = face_cascade.detectMultiScale(frame_gray, scaleFactor=1.3, minNeighbors=5)

    # For each detected rectangle of face, draw a blue rectangle.
    for (x,y,w,h) in faces: 
        #cv2.rectangle(frame_bgr,(x,y),(x+w,y+h),(255,0,0),2)
        
        # Detect smile inside each detected rectangle of face.
        # Draw a green rectangle around each detected smile.
        roi_gray = frame_gray[y:y+h, x:x+w]
        roi_color = frame_bgr[y:y+h, x:x+w]
        smiles = smile_cascade.detectMultiScale(roi_gray, 1.3, 28)
         
        for (sx2, sy2, sw2, sh2) in smiles:
            cv2.rectangle(roi_color, (sx2, sy2), ((sx2 + sw2), (sy2 + sh2)), (0, 0, 255), 2)
            mouse.click(pynput.mouse.Button.left,1)
            #print("Click")
            
    
    #Show FPS
    fc+=1
    TIME = time.time() - start_time

    if (TIME) >= display_time :
        FPS = fc / (TIME)
        fc = 0
        start_time = time.time()

    fps_disp = "FPS: "+str(FPS)[:5]
        
         # Add FPS count on frame
    image = cv2.putText(frame_bgr, fps_disp, (10, 25),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # imshow converts BGR to RGB while saving or displaying.
        #cv2.imshow('Video Stream w/ FPS', image)
    
    cv2.imshow('Live camera + Haar Cascade (face & smile + fist)',frame_bgr)
    if cv2.waitKey(1) == 27:    # Press ESC to exit
        break

cv2.destroyAllWindows()
if camera.isOpened():
    camera.release()
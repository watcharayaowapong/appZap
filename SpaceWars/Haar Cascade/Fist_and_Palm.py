import cv2
import time
import numpy
import pynput.mouse

#To display the video
def showFrame(frame):
    cv2.imshow("frame",frame)
    key= cv2.waitKey(1)
    return key

#Make the rectangle
def make_rect_contours(finder,frame,b,g,r):
    for x,y,w,h in finder:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(b,g,r),3)

def quit(vid):
    vid.release()
    cv2.destroyAllWindows()

#controller object
mouse=pynput.mouse.Controller()

#creates a video capture object. 0 cuz inbuilt camera.
vid=cv2.VideoCapture(0)

check,frame=vid.read()
# frame=cv2.flip(frame,1)

find_fist_init=None

mid_x=0
mid_y=0

#Initial FPS
start_time = time.time()
# FPS update time in seconds
display_time = 2
fc = 0
FPS = 0
########################

while True:
    #Caputures the frame
    frame = vid.read()[1]
    frame = cv2.flip(frame, 1)
    frame_gray=cv2.GaussianBlur(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY),(21,21),0)
    
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


    cascade_hand=cv2.CascadeClassifier("cascade_hand.xml")
    cascade_fist=cv2.CascadeClassifier("cascade_fist.xml")

    find_fist=cascade_fist.detectMultiScale(frame_gray,scaleFactor=1.3,minNeighbors=25)

    # if find_fist is not None:
    #   mouse.click(pynput.mouse.Button.left,1)
        # time.sleep(1)
    if find_fist_init is None:
        find_fist_init=find_fist

    if find_fist ==():
        find_hand=cascade_hand.detectMultiScale(frame_gray,scaleFactor=1.3,minNeighbors=10)

        if find_hand !=():
            mouse.click(pynput.mouse.Button.left,1)
        

    if find_fist != () and find_fist_init!=():
        delx,dely,delw,delh= find_fist[0][0]-find_fist_init[0][0],find_fist[0][1]-find_fist_init[0][1],find_fist[0][2]-find_fist_init[0][2],find_fist[0][3]-find_fist_init[0][3]

        mid_x=(delx+delx+delw)/2
        mid_y=(dely+dely+delh)/2
        mouse.move(-1*7*delx,7*dely)
        # print (find_hand[0][0])

    find_fist_init=find_fist
    #To show the rectangle on the frame
    make_rect_contours(find_fist,frame,255,0,0)
    make_rect_contours(find_hand,frame,0,0,255)
    #frame=cv2.flip(frame,1)
    key=showFrame(frame)

    if(key==ord('x')):
        break


quit(vid)
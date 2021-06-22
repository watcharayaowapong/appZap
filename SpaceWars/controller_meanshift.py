import numpy as np
import cv2
import time
import tkinter as tk
from pynput.mouse import Controller, Button

root = tk.Tk()
m = Controller()


screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


delay = 1       # delay in millisecond for better observation regarding tracking results

# Read the first frame 

capture = cv2.VideoCapture(0)

while True :
    ret,frame = capture.read(0)
    imgH,imgW = frame.shape[0:2]
    frame = cv2.flip(frame,1)
    frame = cv2.resize(frame, (screen_width,screen_height))
    winname = 'Spacebar to capture'
    cv2.imshow(winname,frame)

    if cv2.waitKey( max(1,delay) ) == 32:    # space
        cv2.destroyAllWindows()
        print("capture")
        break

# Select the ROI for histogram backprojection by OpenCV's builtin function
# Try to include only pixels with target colors and avoid including unrelated pixels in this ROI
winname = 'Color template for histogram backproject: drag your ROI and press ENTER'
cv2.imshow(winname,frame)
fromCenter = False          # False = drag a rectangle from the top-left corner to the bottom-right
showCrosshair = False       # False = turn off the crosshair
hist_window = cv2.selectROI(winname,                   # use an existing window instead of ROI selector's window
                            frame,                     # display image
                            showCrosshair, fromCenter )

# Select the ROI for Meanshift's initial window by OpenCV's builtin function
winname = 'Initial search window: drag your ROI and press ENTER'
cv2.imshow(winname,frame)
track_window = cv2.selectROI(winname,                   # use an existing window instead of ROI selector's window
                             frame,                     # display image
                             showCrosshair, fromCenter )

# Convert the two windows to tuples of int as required by cv2.meanShift
hist_window = tuple( [ int(i) for i in hist_window ] )
track_window = tuple( [ int(i) for i in track_window ] )
print('\nThe initial search window was set to',track_window)

# Create the histogram model from the HUE of pixels inside the hist_window
x,y,w,h = hist_window
roi = frame[ y:y+h , x:x+w ]
hsv_roi = cv2.cvtColor( roi, cv2.COLOR_BGR2HSV )
mask = cv2.inRange( hsv_roi,                        # input image
                    np.array((0.,60.,32.)),         # lower bound (avoid false values due to low light)
                    np.array((180.,255.,255.)) )    # upper bound (avoid false values due to low light)
roi_hist = cv2.calcHist( [hsv_roi], [0], mask, [180], [0,180] )
cv2.normalize( roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX )
cv2.imshow('Template color',roi)


# Setup the termination criteria, either finishing 10 iterations or moving by atleast 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

# Initialize the timer
n_frames = 0              # the number of frames
start_time = time.time()  # the start time

print('\nPress ESC at OpenCV window to exit this program ...')

while True:
    ret,frame = capture.read()
    frame = cv2.flip(frame,1)
    frame = cv2.resize(frame, (screen_width,screen_height))
    if ret == False or frame is None:
        break

    # Compute the probability map of the current image
    frame_hsv = cv2.cvtColor( frame, cv2.COLOR_BGR2HSV )
    probMap = cv2.calcBackProject( [frame_hsv],     # input image
                                   [0],                 
                                   roi_hist,        # the reference histogram
                                   [0,180], 1 )
    cv2.imshow('Histogram Back Projection',probMap)

    # Apply meanshift to get the new location
    ret,track_window = cv2.meanShift( probMap, track_window, term_crit )

    # Draw the tracking result 
    x,y,w,h = track_window
    xreal, yreal = (((x+w/2)/imgW)*1920),(((y+h/2)/imgH)*1080)
    print(int(xreal),int(yreal))

    #m.position = xreal, yreal
    m.position = x*1920/640, y*1120/400
    m.position = x,y

    frameResult = cv2.rectangle( frame, (x,y), (x+w,y+h), 255, 2 )
    probmapResult = cv2.rectangle( probMap, (x,y), (x+w,y+h), 255, 2 )

    # Draw a text label specifying the current fps
    n_frames += 1
    total_time = time.time() - start_time
    fps = n_frames / total_time
    h, w, c = frameResult.shape
    caption_h = 40
    frameResult_fps = np.zeros( (h+caption_h,w,c), dtype=np.uint8 )
    frameResult_fps[ caption_h:, ... ] = frameResult
    cv2.putText( frameResult_fps,            # image to draw text
                 f'fps={fps:.2f}',           # text to be written
                 (10,25),                    # position coordinates of the text
                 cv2.FONT_HERSHEY_COMPLEX,   # font type
                 0.75,                       # font scale
                 (255,255,255),              # font BGR color
                 1,                          # font thickness
                 cv2.LINE_AA )
    
    cv2.imshow('Histogram Back Projection',probmapResult)
    cv2.imshow('Mean Shift Tracking',frameResult_fps)

    if cv2.waitKey( max(1,delay) ) == 27:    # ESC
        print("Exit program")
        break
            
cv2.destroyAllWindows()
if capture.isOpened():
    capture.release()

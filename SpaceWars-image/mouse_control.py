import cv2
import time
import mediapipe as mp
import pyautogui as pg

import tkinter as tk

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)
hands = mp_hands.Hands()
pinch_position = []
right_cilck_position = []
direction = [0, 0]
slope = 8
pg.PAUSE = 0
pg.FAILSAFE = True

def moveCurrsor(currPos):
  pg.moveTo(currPos[0], currPos[1])

def getCurrentPosition(landmarks) :
  (h,w,c) = image.shape
  index_position = []
  for index, lm in enumerate(landmarks.landmark) :
    if index == 8 :
      index_position = (lm.x*w, lm.y*h)
      #print('index position is', lm.x*w, lm.y*h)
  return index_position

def moveMode(landmarks) :
  global pinch_position
  (h,w,c) = image.shape
  index_position = []
  middle_position = []
  for index, lm in enumerate(landmarks.landmark) :
    if index == 8 :
      index_position = (lm.x*w, lm.y*h)
      #print('index position is', lm.x*w, lm.y*h)
    if index == 12 :
      middle_position = (lm.x*w, lm.y*h)
      #print('index position is', lm.x*w, lm.y*h)
  if len(index_position) == 2 and len(middle_position) == 2 :
    distance = ((((middle_position[0] - index_position[0] )**2) + ((middle_position[1]-index_position[1])**2) )**0.5)
    #print('distance : ', distance )
    if distance < 50 : 
      if len(pinch_position) == 0 :
        pinch_position = ((middle_position[0]+index_position[0])/2, (middle_position[1]+index_position[1]/2))
      
      return True
    else : return False
  else : return False


def isClick(landmarks) :
  global pinch_position
  (h,w,c) = image.shape
  index_position = []
  thumb_position = []
  for index, lm in enumerate(landmarks.landmark) :
    if index == 5 :
      index_position = (lm.x*w, lm.y*h)
      #print('index position is', lm.x*w, lm.y*h)
    if index == 4 :
      thumb_position = (lm.x*w, lm.y*h)
      #print('index position is', lm.x*w, lm.y*h)
  if len(index_position) == 2 and len(thumb_position) == 2 :
    distance = ((((thumb_position[0] - index_position[0] )**2) + ((thumb_position[1]-index_position[1])**2) )**0.5)
    #print('distance : ', distance )
    if distance < 40 : 
      if len(pinch_position) == 0 :
        pinch_position = ((thumb_position[0]+index_position[0])/2, (thumb_position[1]+index_position[1]/2))
      
      return True
    else : return False
  else : return False

def isRightClick(landmarks) :
  global right_cilck_position
  (h,w,c) = image.shape
  pinky_tip_position = []
  pinky_mcp_position = []
  for index, lm in enumerate(landmarks.landmark) :
    if index == 20 :
      pinky_tip_position = (lm.x*w, lm.y*h)
      #print('index position is', lm.x*w, lm.y*h)
    if index == 17 :
      pinky_mcp_position = (lm.x*w, lm.y*h)
      #print('index position is', lm.x*w, lm.y*h)
  if len(pinky_tip_position) == 2 and len(pinky_mcp_position) == 2 :
    distance = ((((pinky_mcp_position[0] - pinky_tip_position[0] )**2) + ((pinky_mcp_position[1]-pinky_tip_position[1])**2) )**0.5)
    #print('distance : ', distance )
    if distance < 70 : 
      if len(right_cilck_position) == 0 :
        right_cilck_position = ((pinky_mcp_position[0]+pinky_tip_position[0])/2, (pinky_mcp_position[1]+pinky_tip_position[1]/2))
      return True
    else : return False
  else : return False

prevTime = 0
dsize = (int(screen_width*1.2),int(screen_height*1.2))

with mp_hands.Hands(max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.2) as hands:
  while True:
    ret, frame = cap.read() 
    image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    
    image = cv2.resize(image, dsize)
    results = hands.process(image)

    if results.multi_hand_landmarks:
    
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        currPos = getCurrentPosition(hand_landmarks)
        
        if(moveMode(hand_landmarks)):
            moveCurrsor(currPos)
        
        if (isClick(hand_landmarks)) :
          pg.mouseDown()
          print('click')
        else : 
          pg.mouseUp()
          print('release')
          pinch_position = []
        # if (isRightClick(hand_landmarks)) :
        #   pg.rightClick()
        #   print('right click')

    currTime = time.time()
    fps = 1/ (currTime - prevTime)
    prevTime = currTime

    cv2.putText(image,f'FPS : {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 196, 255), 2)

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
import cv2
import time
import mediapipe as mp
import pyautogui as pg


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)
hands = mp_hands.Hands()
pinch_position = []
direction = [0, 0]
slope = 8
pg.PAUSE = 0
pg.FAILSAFE = True



def moveCurrsor(currPos):
  pg.moveTo(currPos[0], currPos[1],)


def changeDirection(pinch_position, curr_pos) :
  if  curr_pos[0] > pinch_position[0] :
    direction[0] = 1
  elif curr_pos[0] == pinch_position[0] :
    direction[0] = 0
  else : direction[0] = -1

  if  curr_pos[1] > pinch_position[1] :
    direction[1] = 1
  elif curr_pos[1] == pinch_position[1] :
    direction[1] = 0
  else : direction[1] = -1

  if pinch_position[0] != curr_pos[0]:
    slope = (curr_pos[1]-pinch_position[1])/(curr_pos[0]-pinch_position[0])



def getCurrentPosition(landmarks) :
  (h,w,c) = image.shape
  index_position = []
  for index, lm in enumerate(landmarks.landmark) :
    if index == 8 :
      index_position = (lm.x*w, lm.y*h)
      #print('index position is', lm.x*w, lm.y*h)
  return index_position

  # def getCurrentPosition(landmarks) :
  # (h,w,c) = image.shape
  # index_position = []
  # thumb_position = []
  # for index, lm in enumerate(landmarks.landmark) :
  #   if index == 8 :
  #     index_position = (lm.x*w, lm.y*h)
  #     #print('index position is', lm.x*w, lm.y*h)
  #   if index == 4 :
  #     thumb_position = (lm.x*w, lm.y*h)
  #     #print('index position is', lm.x*w, lm.y*h)
  # if len(index_position) == 2 and len(thumb_position) == 2 :
  #   return ((thumb_position[0]+index_position[0])/2, (thumb_position[1]+index_position[1]/2))
  # return []

def isPinch(landmarks) :
  global pinch_position
  (h,w,c) = image.shape
  index_position = []
  thumb_position = []
  for index, lm in enumerate(landmarks.landmark) :
    if index == 8 :
      index_position = (lm.x*w, lm.y*h)
      #print('index position is', lm.x*w, lm.y*h)
    if index == 4 :
      thumb_position = (lm.x*w, lm.y*h)
      #print('index position is', lm.x*w, lm.y*h)
  if len(index_position) == 2 and len(thumb_position) == 2 :
    distance = ((((thumb_position[0] - index_position[0] )**2) + ((thumb_position[1]-index_position[1])**2) )**0.5)
    #print('distance : ', distance )
    if distance < 50 : 
      if len(pinch_position) == 0 :
        pinch_position = ((thumb_position[0]+index_position[0])/2, (thumb_position[1]+index_position[1]/2))
      
      return True
    else : return False
  else : return False

prevTime = 0

with mp_hands.Hands(max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.3) as hands:
  while True:
    ret, frame = cap.read() 
    image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)

    if results.multi_hand_landmarks:
    
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        currPos = getCurrentPosition(hand_landmarks)
        #changeDirection(pinch_position, currPos)
        moveCurrsor(currPos)
        if (isPinch(hand_landmarks)) :
          pg.mouseDown()
          print('click')
        else : 
          pg.mouseUp()
          print('release')
          #pinch_position = []
          #direction = [0, 0]

    currTime = time.time()
    fps = 1/ (currTime - prevTime)
    prevTime = currTime

    cv2.putText(image,f'FPS : {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 196, 255), 2)

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
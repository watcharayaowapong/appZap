import cv2
import time
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)
hands = mp_hands.Hands()

prevTime = 0

with mp_hands.Hands(max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.1) as hands:
  while True:
    ret, frame = cap.read() 
    image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)

    if results.multi_hand_landmarks:
    
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)


    currTime = time.time()
    fps = 1/ (currTime - prevTime)
    prevTime = currTime

    cv2.putText(image,f'FPS : {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 196, 255), 2)

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
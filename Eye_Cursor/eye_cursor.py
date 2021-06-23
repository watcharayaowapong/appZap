import cv2
import numpy as np
import dlib
import time
from pynput.mouse import Controller, Button
import tkinter as tk

root = tk.Tk()
m = Controller()

# get maximum screen height/width
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


# Display framerate
start_time = time.time()
display_time = 2
fc = 0
FPS = 0

# Counter for when to update eye_frame
counter = 0

# Blob Detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

blob_detector_params = cv2.SimpleBlobDetector_Params()
blob_detector_params.filterByArea = True
blob_detector_params.maxArea = 1500 #1500
blob_detector_params.filterByConvexity = True
blob_detector_params.minConvexity = 0.6
blob_detector = cv2.SimpleBlobDetector_create(blob_detector_params)

def blob_process(img, detector):
    # gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # _, img = cv2.threshold(gray_frame, 42, 255, cv2.THRESH_BINARY)
    img = cv2.erode(img, None, iterations=2) #1
    img = cv2.dilate(img, None, iterations=4) #2
    img = cv2.medianBlur(img, 5) #3
    keypoints = detector.detect(img)
    return keypoints

# binary threshold control for when to cropped eye image
def threshold_eye(eye_frame):
    return cv2.threshold(eye_frame, 130, 255, cv2.THRESH_BINARY)

# transform poit in perspective1 to perspective2
def transform_point(x,y, matrix):
    p = (x,y)
    px = (matrix[0][0]*p[0] + matrix[0][1]*p[1] + matrix[0][2]) / ((matrix[2][0]*p[0] + matrix[2][1]*p[1] + matrix[2][2]))
    py = (matrix[1][0]*p[0] + matrix[1][1]*p[1] + matrix[1][2]) / ((matrix[2][0]*p[0] + matrix[2][1]*p[1] + matrix[2][2]))
    p_after = (int(px), int(py))

    return p_after


def calibrate():
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        for face in faces:
            landmarks = predictor(gray, face)

            top = landmarks.part(37).y
            bottom = landmarks.part(40).y
            left = landmarks.part(36).x
            right = landmarks.part(39).x
        try:
            eye_frame = gray[top-10:bottom+10, left-5:right+5]
            _, eye_frame = threshold_eye(eye_frame)
            # eye_frame = cv2.erode(img, None, iterations=4)
            # eye_frame = cv2.dilate(img, None, iterations=1)
            # eye_frame = cv2.erode(img, None, iterations=2)


            keypoints = blob_process(eye_frame, blob_detector)
            eye_frame = cv2.drawKeypoints(eye_frame, keypoints, eye_frame, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            if len(keypoints) == 1:
                print('blob found')
                old_keypoints = keypoints[0].pt
            else:
                # try:
                print('blob not found')

        except:
            pass

        cv2.imshow("calibrate", eye_frame)

        key = cv2.waitKey(1)
        if key == 27:
            break

    return old_keypoints






print("Calibrating top left corner")
print('Press ESC when done')
topleft = calibrate()

print("Calibrating top right corner")
print('Press ESC when done')
topright = calibrate()

print("Calibrating bottom left corner")
print('Press ESC when done')
bottomleft = calibrate()

print("Calibrating top right corner")
print('Press ESC when done')
bottomright = calibrate()


pers1=np.float32([[topleft[0],topleft[1]],[topright[0],topright[1]],[bottomleft[0],bottomleft[1]],[bottomright[0],bottomright[1]]]) 
pers2=np.float32([[0,0],[screen_width,0],[0,screen_height],[screen_width,screen_height]])
matrix=cv2.getPerspectiveTransform(pers1,pers2)

print()
print()
print('Entering Main Loop')
print()
print()

cap = cv2.VideoCapture(0)

while True:


    _, frame = cap.read()

    fc+=1
    TIME = time.time() - start_time
    if (TIME) >= display_time:
        FPS = fc / (TIME)
        fc = 0
        start_time = time.time() 
    fps_disp = ""+str(FPS)[:2] # Add FPS count on frame

    # Webcam image pre-processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray, (5,5), 0)
    # gray = cv2.blur(gray, (5,5))

    faces = detector(gray)

    for face in faces:
        if counter % 120 == 0:
            # print('pass')
            counter+= 1      
            pass

        else:
            # print(counter)
            # print('break')
            counter+= 1
            break

        landmarks = predictor(gray, face)

        top = landmarks.part(37).y
        bottom = landmarks.part(40).y
        left = landmarks.part(36).x
        right = landmarks.part(39).x


    try:
        eye_frame = gray[top-10:bottom+10, left-5:right+5]
        _, eye_frame = threshold_eye(eye_frame)
        # eye_frame = cv2.erode(img, None, iterations=4)
        # eye_frame = cv2.dilate(img, None, iterations=1)
        # eye_frame = cv2.erode(img, None, iterations=2)


        keypoints = blob_process(eye_frame, blob_detector)
        eye_frame = cv2.drawKeypoints(eye_frame, keypoints, eye_frame, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        print(counter)

        if len(keypoints) == 1:
            # pointer = transform_point(keypoints[0].pt[0], keypoints[0].pt[1])
            # print('x,y', keypoints[0].pt)
            # print('blob found')
            # print('len==1')
            pointer = transform_point(keypoints[0].pt[0], keypoints[0].pt[1], matrix)
            old_keypoints = keypoints[0].pt
            # print('len==1 finish')
        else:
            # try:
            # print('blob not found')
            pointer = transform_point(old_keypoints[0].pt[0], old_keypoints[0].pt[1], matrix)
            # print('blob not found finish')
            # pointer = transform_point(old_keypoints[0].pt[0], old_keypoints[0].pt[1])


        # m.position = transform_point(keypoints[0].pt[0], keypoints[0].pt[1], matrix)
        m.position = pointer[0], pointer[1]
        print(m.position)
        # if counter > 10:
        #     # try:
        #     #     print(topleft)
        #     #     break
        #     # except:
        #     print('Please look on Top-Left corner')

        #     print(keypoints[0].pt)
        #     topleft = keypoints[0].pt
        #     print(keypoints[0].pt)
            

    except:
        pass


    cv2.imshow("eye", eye_frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()




#             try:
#                 print(topleft)
#                 break
#             except:
#                 print('Please look on Top-Left corner')
#                 countdown(4)
#                 topleft = keypoints[0].pt
#                 pass

#             # try:
#             #     topright
#             # except:
#                 print('Please look on Top-Right corner')
#                 countdown(4)
#                 topright = keypoints[0].pt
#                 pass

#             try:
#                 bottomleft
#             except:
#                 print('Please look on Bottom-Left corner')
#                 countdown(4)
#                 bottomleft = keypoints[0].pt
#                 pass

#             try:
#                 bottomright
#             except:
#                 print('Please look on Bottom-Right corner')
#                 countdown(4)
#                 bottomright = keypoints[0].pt

#                 pers1=np.float32([[topleft[0],topleft[1]],[topright[0],topright[1]],[bottomleft[0],bottomleft[1]],[bottomright[0],bottomright[1]]]) 
#                 pers2=np.float32([[0,0],[screen_width,0],[0,screen_height],[screen_width,screen_height]])
#                 matrix=cv2.getPerspectiveTransform(pts1,pts2)
#                 pass



#     # cv2.imshow("eye", eye_frame)

#     key = cv2.waitKey(1)
#     if key == 27:
#         break


# cap.release()
# cv2.destroyAllWindows()








# while True:

#     print('real while loop')
#     print('real while loop')
#     print('real while loop')
#     print('real while loop')
#     print('real while loop')
#     print('real while loop')
#     print('real while loop')
#     _, frame = cap.read()

#     fc+=1
#     TIME = time.time() - start_time
#     if (TIME) >= display_time:
#         FPS = fc / (TIME)
#         fc = 0
#         start_time = time.time() 
#     fps_disp = ""+str(FPS)[:2] # Add FPS count on frame



#     # Webcam image pre-processing
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     # gray = cv2.GaussianBlur(gray, (5,5), 0)
#     # gray = cv2.blur(gray, (5,5))


#     faces = detector(gray)


#     for face in faces:

#         if counter % 120 == 0:
#             # print('pass')
#             counter+= 1      
#             pass

#         else:
#             # print(counter)
#             # print('break')
#             counter+= 1
#             break

#         # x1 = face.left()
#         # y1 = face.top()
#         # x2 = face.right()
#         # y2 = face.bottom()
#         #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

#         landmarks = predictor(gray, face)

#         # left_point = (landmarks.part(36).x, landmarks.part(36).y)
#         # right_point = (landmarks.part(39).x, landmarks.part(39).y)

#         # center_top = midpoint(landmarks.part(37), landmarks.part(38))
#         # center_bottom = midpoint(landmarks.part(41), landmarks.part(40))
#         # hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
#         # ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)

#         top = landmarks.part(37).y
#         bottom = landmarks.part(40).y
#         left = landmarks.part(36).x
#         right = landmarks.part(39).x

#         print('point1')
#         # if top is None:
#         #     top = landmarks.part(37).y
#         #     bottom = landmarks.part(40).y
#         #     left = landmarks.part(36).x
#         #     right = landmarks.part(39).x

#         # top_old = top


#         # print(f'top: {top}')
#         # print(f'bottom: {bottom}')
#         # print(f'left: {left}')
#         # print(f'right: {right}')
#         # print()

#         # frame = faces[landmarks.part(37).y - 10: landmarks.part(40).y + 10, landmarks.part(36).x - 10 : landmarks.part(39).x + 10 ]

#     # if top is not None:
#     try:
#         # eye_frame = gray[top:bottom, left:right]
#         eye_frame = gray[top-10:bottom+10, left-5:right+5]
#         _, eye_frame = threshold_eye(eye_frame, 120) #cv2.threshold(eye_frame, 130, 255, cv2.THRESH_BINARY)
#         # eye_frame = cv2.erode(img, None, iterations=4)
#         # eye_frame = cv2.dilate(img, None, iterations=1)
#         # eye_frame = cv2.erode(img, None, iterations=2)


#         keypoints = blob_process(eye_frame, blob_detector)
#         eye_frame = cv2.drawKeypoints(eye_frame, keypoints, eye_frame, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

#         # print(len(keypoints))

#         # try:
#         #     topleft
#         # except:
#         #     print('Please look on Top-Left corner')
#         #     countdown(4)
#         #     topleft = keypoints[0].pt

#         # try:
#         #     topright
#         # except:
#         #     print('Please look on Top-Right corner')
#         #     countdown(4)
#         #     topright = keypoints[0].pt

#         # try:
#         #     bottomleft
#         # except:
#         #     print('Please look on Bottom-Left corner')
#         #     countdown(4)
#         #     bottomleft = keypoints[0].pt

#         # try:
#         #     bottomright
#         # except:
#         #     print('Please look on Bottom-Right corner')
#         #     countdown(4)
#         #     bottomright = keypoints[0].pt

#             # pers1=np.float32([[topleft[0],topleft[1]],[topright[0],topright[1]],[bottomleft[0],bottomleft[1]],[bottomright[0],bottomright[1]]]) 
#             # pers2=np.float32([[0,0],[screen_width,0],[0,screen_height],[screen_width,screen_height]])
#             # matrix=cv2.getPerspectiveTransform(pts1,pts2)


    
#         if len(keypoints) == 1:
#             pointer = transform_point(keypoints[0].pt[0], keypoints[0].pt[1])
#             m.position = pointer
#             # print('x,y', keypoints[0].pt)
#             old_keypoints = keypoints[0].pt
#         else:
#             # try:
#             print('blob not found')
#             pointer = transform_point(old_keypoints[0].pt[0], old_keypoints[0].pt[1])
#             m.position = pointer
#             # print('x,y old', old_keypoints)
#             # except:
#             #     pass

#     except:
#         pass

#         # for n in range(0, 68):
#         #     x = landmarks.part(n).x
#         #     y = landmarks.part(n).y
#         #     cv2.circle(frame, (x, y), 4, (255, 0, 0), -1)

#     # print(eye_frame.shape)
#     # eye_frame = imutils.resize(eye_frame, width=500)
#     eye_frame = cv2.resize(eye_frame  , (eye_frame.shape[1]*5 , eye_frame.shape[0]*5))
#     eye_frame = cv2.putText(eye_frame, fps_disp, (2, 8),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2) # imshow converts BGR to RGB while saving or displaying.


#     # cv2.imshow("gray", gray)
#     # cv2.imshow("blur1", blur1)
#     # cv2.imshow("blur2", blur2)
#     cv2.imshow("eye", eye_frame)

#     key = cv2.waitKey(1)
#     if key == 27:
#         break


# cap.release()
# cv2.destroyAllWindows()
import cv2
import numpy as np
import dlib
import time
import math
from eye_1_functions import Calibration,center_detect


center_pt=[]
calib=False

def roi():
    global landmarks
    #----------------------draw rectagle over eyes--------------------------------------------------------------- 
    x_36,y_36=landmarks.part(36).x , landmarks.part(36).y
    x_39,y_39=landmarks.part(39).x , landmarks.part(39).y
    #ratios
    h=x_39-x_36 # eye width
    w=int(1.5*h)
    rx,ry=x_36-int(h/3),y_36-int(h/2)
    cv2.rectangle(frame,(rx,ry), (rx+w,ry+h), (0, 255, 0), 1)
    print(h,"  ",w)

    eye=gray[ry:ry+h,rx:rx+w]# region
    return eye


def draw():
    #---------------drawing line_---------------------------------------------------------        
    for n in range(37, 48):
        if n == 42: # skip the midle line
            continue
        x = landmarks.part(n).x
        y = landmarks.part(n).y
            #### drawing line from n-1 to n ###########################
        cv2.line(frame,(landmarks.part(n-1).x,landmarks.part(n-1).y),(x,y),(0,255,0),1)
        cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

        #----------to complete 41 to back 36    and 47 to 42
    cv2.line(frame,(landmarks.part(36).x,landmarks.part(36).y),
                 (landmarks.part(41).x,landmarks.part(41).y),(0,255,0),1)
    cv2.line(frame,(landmarks.part(42).x,landmarks.part(42).y),
                 (landmarks.part(47).x,landmarks.part(47).y),(0,255,0),1)

    

#-----------------------------------------------------------------------------------
cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


last_time=time.time()
while True:
    _, frame = cap.read()
    frame=cv2.flip(frame,1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()
        #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

        landmarks = predictor(gray, face)
    
    eye_img=roi()

    center,thresh=center_detect(eye_img)
    #center_pt.append(center)
    
    if(calib==True):
        
        map=Calibration(center,thresh)
        calib=True
    
    draw()
    
    cv2.imshow("Threshold", thresh)
    cv2.imshow("Roi", eye_img)
    #cv2.imshow("Frame", frame)
    
    #frame rate
    print("time = {}".format(time.time()-last_time))
    last_time=time.time()
    ##
    key = cv2.waitKey(1)
    if key == 27:
        break

#print(max(center_pt))
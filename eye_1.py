import cv2
import numpy as np
import dlib
import time
import math
#get screen size
from win32api import GetSystemMetrics
Width =GetSystemMetrics(0)
Height =GetSystemMetrics(1)

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
    #print(h,"  ",w)

    eye=gray[ry:ry+h,rx:rx+w]# region
    return eye

def center_detect(image):
    #############################################
    rows, cols = eye_img.shape
    #gray_roi = cv2.cvtColor(eye_img, cv2.COLOR_BGR2GRAY)
    gray_roi = cv2.GaussianBlur(eye_img, (7, 7), 0)
    
    _, threshold = cv2.threshold(gray_roi, 25, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        #cv2.drawContours(roi, [cnt], -1, (0, 0, 255), 3)
        #cv2.rectangle(eye_img, (x, y), (x + w, y + h), (255, 0, 0), 1)

        cv2.circle(eye_img, (x+int(w/2), y+int(h/2)), 2, (0, 0, 255), -1)
        cv2.line(eye_img, (x + int(w/2), 0), (x + int(w/2), rows), (0, 255, 0), 1)
        cv2.line(eye_img, (0, y + int(h/2)), (cols, y + int(h/2)), (0, 255, 0), 1)
        break
    
    center=[x+int(w/2), y+int(h/2)]
    
    cv2.imshow("Threshold", threshold)
    cv2.imshow("Roi", eye_img)
    
    return center
##########################################

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

    



def calibrations():
    global eye,Width,Height
    test=np.ones([Height,Width]) # width , height
    cv2.putText(test, 'Initiating calibration', (200,200), cv2.FONT_HERSHEY_SIMPLEX,3, (0, 0, 255), 5, cv2.LINE_AA) 
    cv2.putText(test, 'Follow the Instruction', (200,300), cv2.FONT_HERSHEY_SIMPLEX,3, (0, 0, 255), 5, cv2.LINE_AA)
    cv2.imshow("calibration", test)
    time.sleep(5)
    test=np.ones([Height,Width])
    cv2.imshow("calibration", test)


#-----------------------------------------------------------------------------------
cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

calib=False
last_time=time.time()
while True:
    _, frame = cap.read()
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

    center_detect(eye_img)

    draw()
    if(calib==True):
        calibrations()
        calib=True

    cv2.imshow("Frame", frame)
    #cv2.imshow("image", image)
    #frame rate
    print("time = {}".format(time.time()-last_time))
    last_time=time.time()
    ##
    key = cv2.waitKey(1)
    if key == 27:
        break

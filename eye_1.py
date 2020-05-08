import cv2
import numpy as np
import dlib

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

    #----------------------draw rectagle over eyes--------------------------------------------------------------- 
    leye_x1,leye_y1=landmarks.part(36).x , landmarks.part(36).y
    leye_x2,leye_y2=landmarks.part(41).x , landmarks.part(41).y
    cv2.rectangle(frame,(leye_x1-10,leye_y1-20), (leye_x2+40,leye_y2+10), (0, 255, 0), 1)




cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

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
        draw()

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

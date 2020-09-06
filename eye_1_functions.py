import numpy as np
import cv2
import time

def center_detect(image):
    #############################################
    eye_img=image
    rows, cols = eye_img.shape
    #gray_roi = cv2.cvtColor(eye_img, cv2.COLOR_BGR2GRAY)

    gray_roi = cv2.GaussianBlur(eye_img, (7, 7), 0)
    _, threshold = cv2.threshold(gray_roi, 25, 255, cv2.THRESH_BINARY_INV)
    #_,threshold = cv2.threshold(gray_roi,25,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    if contours:
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            #cv2.drawContours(roi, [cnt], -1, (0, 0, 255), 3)
            #cv2.rectangle(eye_img, (x, y), (x + w, y + h), (255, 0, 0), 1)

            cv2.circle(eye_img, (x+int(w/2), y+int(h/2)), 2, (0, 0, 255), -1)
            cv2.line(eye_img, (x + int(w/2), 0), (x + int(w/2), rows), (0, 255, 0), 1)
            cv2.line(eye_img, (0, y + int(h/2)), (cols, y + int(h/2)), (0, 255, 0), 1)
            center=[x+int(w/2), y+int(h/2)]

            return center,threshold
    else:
        return _,threshold
    '''
    kernel = np.ones((3, 3), np.uint8)
    eye_img = cv2.bilateralFilter(eye_img, 10, 15, 15)
    eye_img = cv2.erode(eye_img, kernel, iterations=3)
    threshold = cv2.adaptiveThreshold(eye_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY_INV,11,2)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    contours = sorted(contours, key=cv2.contourArea)
    if contours:
        try:
            moments = cv2.moments(contours[-2])
            x = int(moments['m10'] / moments['m00'])
            y = int(moments['m01'] / moments['m00'])
            center=[x,y]
            cv2.circle(eye_img, (x,y), 3, (255, 255, 255), -1)
            print(center)
            return center,threshold
        except (IndexError, ZeroDivisionError):
            pass
    else:
        return _,threshold'''
##########################################

def Calibration(center,image):
    thr_eye=image
    #get screen size
    from win32api import GetSystemMetrics
    Width =GetSystemMetrics(0)
    Height =GetSystemMetrics(1)


    c=0
    rect=[]

    while(1):
        test=np.ones([Height,Width])
        #test=image
        if c==0:
            c=c+1
        elif c==1:
            cv2.putText(test, 'Initiating calibration', (200,200), cv2.FONT_HERSHEY_SIMPLEX,3, (0, 0, 255), 5, cv2.LINE_AA) 
            cv2.putText(test, 'Follow the Instruction', (200,300), cv2.FONT_HERSHEY_SIMPLEX,3, (0, 0, 255), 5, cv2.LINE_AA)
            time.sleep(3)
            center_detect(thr_eye)
            
            c=c+1
        elif c ==2:
            cv2.putText(test, 'look at top left corner', (200,300), cv2.FONT_HERSHEY_SIMPLEX,3, (0, 0, 255), 5, cv2.LINE_AA) 
            cv2.circle(test,(0,0),100,(0,0,0),-1)
            time.sleep(3)
            center_detect(thr_eye)
            
            c=c+1
        elif c ==3:
            cv2.putText(test, 'look at top right corner', (200,300), cv2.FONT_HERSHEY_SIMPLEX,3, (0, 0, 255), 5, cv2.LINE_AA) 
            cv2.circle(test,(Width,0),100,(0,0,0),-1)
            time.sleep(3)
            center_detect(thr_eye)
            
            c=c+1
        elif c ==4:
            cv2.putText(test, 'look at bottom right corner', (200,300), cv2.FONT_HERSHEY_SIMPLEX,3, (0, 0, 255), 5, cv2.LINE_AA) 
            cv2.circle(test,(Width,Height),100,(0,0,0),-1)
            time.sleep(3)
            center_detect(thr_eye)
            
            c=c+1
        elif c==5:
            cv2.putText(test, 'look at bottom left corner', (200,300), cv2.FONT_HERSHEY_SIMPLEX,3, (0, 0, 255), 5, cv2.LINE_AA) 
            cv2.circle(test,(0,Height),100,(0,0,0),-1)
            time.sleep(3)
            center_detect(thr_eye)
            
            c=c+1
        elif c==6:
            cv2.putText(test, 'done use the mouse', (200,300), cv2.FONT_HERSHEY_SIMPLEX,3, (0, 0, 255), 5, cv2.LINE_AA) 
            time.sleep(3)
            cv2.destroyWindow('calib')
            return 1

        #cv2.imshow("thresh", thr_eye)
        cv2.imshow("calib", test)
        key = cv2.waitKey(1)
        if key == 27:
            break

    #time.sleep(5)
    #test=np.ones([Height,Width])
    #cv2.imshow("calib", test)


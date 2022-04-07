from AlphaBot import AlphaBot

import cv2 as cv
from time import sleep

car = AlphaBot()

capture = cv.CaptureFromCAM(0)
cv.SetCaptureProperty(capture, 3, 160)
cv.SetCaptureProperty(capture, 4, 120)


while True:
    img = cv.QueryFrame(capture)
    
    cv.Smooth(img, img, cv.CV_BLUR,3)
    hue_img = cv.CreateImage(cv.GetSize(img), 8, 3)
    cv.CvtColor(img, hue_img, cv.CV_BGR2HSV)

        #(38,120,60)(75,255,255)#(90,103,130), (145,255,255)
        #150,100,50, 215,245,255
    threshold_img = cv.CreateImage(cv.GetSize(img),8 ,1)#blue
    cv.InRangeS(hue_img, (80,90,90), (135,185,255), threshold_img)
                    #(38,120,60)(75,255,255)#(65,95,130), (125,190,255)

    storage = cv.CreateMemStorage(0)
    contour = cv.FindContours(threshold_img, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)

    points = []
    while contour:
        rect = cv.BoundingRect(list(contour))
        contour = contour.h_next()
        size  = (rect[2] * rect[3])
        mid = (rect[0]+rect[2]/2)
        diag = (rect[2]**2 + rect[3]**2)**0.5
        
        if (size > 100):
            pt1 = (rect[0], rect[1]) #left top
            pt2 = (rect[0]+rect[2], rect[1]+rect[3])  #right bottom
            cv.Rectangle(img, pt1, pt2, (255,0,0),3)
                
            #print(str(pt1)+str(pt2)+str(size)+' '+str(diag))
            #print(str(diag)) 	
                        #if (rect[0]+rect[2]/2) > 80:
            sleep(0.01)
            if mid > 100:#turn right
                car.right()
                print('right')
            elif mid < 60:#turn left
                car.left()
                print('left')
            elif diag > 100:#back
                car.backward()
                print('backword')
            elif diag < 80:#for
                car.forward()
                print('forword')
            else:
                car.stop()
                print('stop')
                sleep(0.01)
        else:
                car.stop()
                sleep(0.01)

        cv.ShowImage("Colour Tracking", img)
    #cv.ShowImage("Threshold", threshold_img)

    if cv.WaitKey(10) == 27:
        break

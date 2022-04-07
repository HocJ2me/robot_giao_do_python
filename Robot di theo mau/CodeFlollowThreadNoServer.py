import cv2
import numpy as np
from PIL import Image
import time
from AlphaBot import AlphaBot
from threading import Thread
import socket #ip
#--------------initialise motor speed-----------------------------------
robot = AlphaBot()

robotState = 0 #stop
lastRobotState = 0
#---------------------------------------------------------------
cap = cv2.VideoCapture(0)
image_width = 640
image_height = 480
HUE_VAL = 170
center_image_x = image_width / 2
center_image_y = image_height / 2
minimum_area = 250
maximum_area = 100000
lower_color = np.array([HUE_VAL-10,100,100])
upper_color = np.array([HUE_VAL+10, 255, 255])

def move_robot(ball_location):
    global robotState
    global lastRobotState
    if ball_location:
        if (ball_location[0] > minimum_area) and (ball_location[0] < maximum_area):
            if ball_location[1] < ((image_width/3)):
                robotState = 2
            elif (ball_location[1] > (image_width/3)) and (ball_location[1] < (image_width - (image_width/3))):
                robotState = 0
            else:
                robotState = 3
        elif (ball_location[0] < minimum_area):
            robot.stop()
            print("Target isn't large enough, searching")
            robotState = 4
        else:
            print("Target large enough, stopping")
            robotState = 1
    else:
        robot.stop()
        print("Target not found, searching")
    if(lastRobotState != robotState):
        lastRobotState = robotState        
        if(robotState == 0):
            print("Forward")
            robot.forward()
        elif(robotState == 1):
            robot.backward()
        elif(robotState == 2):
            robot.left()
            print("Turning left")
        elif(robotState == 3):
            robot.right()
            print("Turning right")
        elif(robotState == 4):
            robot.stop()
def draw_line(im):
    cv2_im = im
    height, width, channels = im.shape
    #draw center cross lines
    cv2_im = cv2.rectangle(cv2_im, (0,int(height/3)-1)
                           , (width, int(height/3)+1)
                           , (255,0,0), -1)
    cv2_im = cv2.rectangle(cv2_im, (int(width/3)-1,0)
                           , (int(width/3)+1,height)
                           , (255,0,0), -1)
    cv2_im = cv2.rectangle(cv2_im, (int(width/3)*2-1,0)
                           , (int(width/3)*2+1,height)
                           , (255,0,0), -1)
    cv2_im = cv2.rectangle(cv2_im, (int(width/2)-1,0)
                           , (int(width/2)+1,height)
                           , (255,0,0), -1)
    return cv2_im
def main():
    while True:
        ret, image = cap.read()    
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#         cv2.imshow("ORIGINAL",image)
        color_mask = cv2.inRange(hsv, lower_color, upper_color)    
        countours, hierarchy = cv2.findContours(color_mask
                                                , cv2.RETR_LIST
                                                , cv2.CHAIN_APPROX_SIMPLE)        
        
        result = cv2.bitwise_and(image, image, mask= color_mask)
        result = draw_line(result)
        object_area = 0
        object_x = 0
        object_y = 0
        object_w = 0
        object_h = 0
        for contour in countours:
            x, y, width, height = cv2.boundingRect(contour)
            found_area = width * height
            center_x = x + (width / 2)
            center_y = y + (height / 2)
            if object_area < found_area:
                object_area = found_area
                object_x = center_x
                object_y = center_y
                object_w = width
                object_h = height
        if object_area > 0:
            ball_location = [object_area, int(object_x), int(object_y)
                             , int(object_w), int(object_h)]
            result = cv2.circle(result, (int(object_x)+1, int(object_y)+1), 20, (0, 0, 255), -1)

        else:
            ball_location = None
        thread = Thread(target = move_robot(ball_location))
        thread.start()
        cv2.imshow("result",result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    main()

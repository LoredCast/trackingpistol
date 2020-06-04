import cv2
import numpy as np
import serial
import time
import sys
import controller
import random


face_cascade = cv2.CascadeClassifier("venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
profile_cascade = cv2.CascadeClassifier("venv/Lib/site-packages/cv2/data/haarcascade_profileface.xml")

cap = cv2.VideoCapture(0)
FRAME_WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
FRAME_HIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
RATE = cap.get(cv2.CAP_PROP_FPS)

####### Constants ###### 

CENTER_Y = 90
CENTER_X = 90
MARGIN = 5
SPEED = 0.2
ANGLE_PER_STEP = 1.8 #  Depending on Stepper


####### Tracking algorithm things for the motors #######


def servo_xangle(xpos, fov_offset=70):  #  function for when camera is stationary
    scale = (90 - fov_offset) / (FRAME_WIDTH / 2)
    angle = xpos * scale + fov_offset
    
    return int(angle)


def servo_yangle(ypos, fov_offset=70): #  function for when camera is stationary
    scale = (90 - fov_offset) / (FRAME_HIGHT / 2)
    angle = ypos * scale + fov_offset
    if angle < 85:
        return 85
    else:
        return int(angle)


#  Track Y tracks the displacement of the center of the face relative to the image center
#  and creates an angle which is scaled according to the viewport
#  This angle gets added to the current angle Y to make up the angle sent to the servo

currentangleY = 90

def trackY(ypos, fov_offset):
    global currentangleY
    global SPEED
    scale = (90 - fov_offset) / (FRAME_HIGHT / 2)
    displacement_angle = (ypos - (FRAME_HIGHT / 2)) * scale

    if displacement_angle > displacement_angle * SPEED:
        displacement_angle *= SPEED
    elif displacement_angle < displacement_angle * SPEED:
        displacement_angle *= SPEED


    displacement_angle *= -1 #  flipped the angle because servo got Mounted the other way

    offpixel = (FRAME_HIGHT/2) -  ypos

    if offpixel > MARGIN or offpixel < -MARGIN: #  when out of center MARGIN: reposition
        currentangleY += displacement_angle
        if currentangleY < 60:
            return 60
        elif currentangleY > 180:
            return 180
        else:
            return int(currentangleY)




#  Track X tracks the displacement of the center of the face relative to the image center
#  and creates an angle which is scaled according to the viewport
#  This angle gets added to the current angle X to make up the angle sent to the servo

currentangleX = 90

def trackX(xpos, fov_offset): 
    global currentangleX
    global SPEED

    scale = (90 - fov_offset) / (FRAME_WIDTH / 2)
    displacement_angle = (xpos - (FRAME_WIDTH / 2)) * scale

    if displacement_angle > displacement_angle * SPEED:
        displacement_angle *= SPEED
    elif displacement_angle < displacement_angle * SPEED:
        displacement_angle *= SPEED


    offpixel = (FRAME_WIDTH/2) - xpos

    if offpixel > MARGIN or offpixel < -MARGIN:
        currentangleX += displacement_angle
        if currentangleX <= 0:
            return 0
        elif currentangleX > 180:
            return 180
        else:
            return int(currentangleX)

#  only track the desiplacement
#  is used for steppermotors, does the same as TrackX but without the counter

def trackXdisp(xpos, fov_offset):
    global currentangleX
    global SPEED

    scale = (90 - fov_offset) / (FRAME_WIDTH / 2)
    displacement_angle = (xpos - (FRAME_WIDTH / 2)) * scale
    
    return int(displacement_angle/ANGLE_PER_STEP)


currentStepperAngle = 90

patrolStateX = 0
patrolStateY = currentangleY
directionX = 1
directionY = 1

def patrol(speedX, speedY):
    global directionX
    global directionY
    global currentStepperAngle
    global patrolStateX
    global patrolStateY
    global currentangleY
    
    

    if currentangleY > 120:
        directionY = -1
    elif currentangleY < 60:
        directionY = 1
    elif currentangleY % 5 == 0:
        rand = random.randint(0, 1)
        if rand == 1:
            directionY = 1
        if rand == 0:
            directionY = -1
    
    currentangleY += directionY * speedY
    

    turret.gotoY(currentangleY)

    if currentStepperAngle > 120:
        directionX = -1
    elif currentStepperAngle < 60: 
        directionX = 1

    currentStepperAngle += directionX * speedX

    
    
    turret.step(directionX * speedX)

    





######## The Face Tracking ########
cv2.namedWindow("win", cv2.WINDOW_FREERATIO)
idleFrameCount = 0


patrolAwait = 20
class Tracker:
    
    
    mouth_xy = (0,0)
    
    Tracking = True
    def setTracking(self, state = True):
        self.Tracking = state

    def mainloop(self, show_Boxes = True):

        global idleFrameCount
        

        while self.Tracking:
            
            
            
            ret, img = cap.read()

            cv2.resizeWindow("win", (int(FRAME_WIDTH * 1.5), int(FRAME_HIGHT * 1.5)))

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            grayinverse = cv2.flip(gray, 1) #  flipped image for profiles
            faces = face_cascade.detectMultiScale(gray, 1.2, 5, minSize=(13,13))

            

            if len(faces) == 0: #  if no faces detected, try profiles first on normal than flipped
                faces = profile_cascade.detectMultiScale(gray, 1.2, 5, minSize=(13,13))
                if len(faces) == 0:
                    faces = profile_cascade.detectMultiScale(grayinverse, 1.2, 5, minSize=(13,13))
                    if len(faces) == 0:
                        idleFrameCount += 1
                    else:
                        for i in range(len(faces)):  #  flip coordinates 
                            faces[i][0] = FRAME_WIDTH - faces[i][0]
                            faces[i][2] = -faces[i][2]

            

            if len(faces) != 0:
                idleFrameCount = 0

            if idleFrameCount > patrolAwait:
                patrol(1, 2)

            
            
            for (x, y, w, h) in faces:
                if show_Boxes:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

                roi_gray = gray[y:y + h, x:x + h]
                roi_color = img[y:y + h, x:x + h]

                mouth_xy = (int(x + (w/2)), int(y + (0.25 * h)))
                cv2.circle(img, mouth_xy, 2, (255, 0, 0), 2)
                    



                # xpos = trackX(mouth_xy[0], 70) #  only if x is a Servo
                ypos = trackY(mouth_xy[1], 70) 
                xstep = trackXdisp(mouth_xy[0], 70)
                
                turret.gotoY(ypos)
                turret.step(-xstep) #  flip step for right direction









                ######## debug info #########

                sys.stdout.write("\r" + "mouth @ x: " + str(mouth_xy[0]) + " | "+  str(-xstep) + "steps in x || y: " + str(mouth_xy[1]) + " | " + str(ypos) + "°")
                
                
            cv2.imshow("win", img)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
        

if __name__ == "__main__":
    turret = controller.Turret("COM6")
    Tracker = Tracker()
    Tracker.mainloop()
    print("\nStarting the engines...\n")
import win32com.client as wincl
import cv2
import numpy as np
import threading
import math




show_Boxes = True

face_cascade = cv2.CascadeClassifier("venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("venv/Lib/site-packages/cv2/data/haarcascade_eye.xml")
smile_cascade = cv2.CascadeClassifier("venv/Lib/site-packages/cv2/data/haarcascade_smile.xml")
profile_cascade = cv2.CascadeClassifier("venv/Lib/site-packages/cv2/data/haarcascade_profileface.xml")

cap = cv2.VideoCapture(0)
fram_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

import serial
import time

serial = serial.Serial("COM3", 9800, timeout=1)

class Servo:
    def __init__(self, index):
        Servo.index = index

    def goto(self, pos):
        serial.write(chr(pos).encode("utf-8"))



def servo_xangle(xpos, fov_offset=70):
    scale = (90 - fov_offset) / (fram_width / 2)
    angle = xpos * scale + fov_offset
    
    return int(angle)
    

Servo1 = Servo(1)




class ft:
    def __init__(self):
        self.mouth = (0,0)
    



    def cv(self):
        while True:
            
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # smiles = smile_cascade.detectMultiScale(gray, 1.8, 20)

            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            #profiles = profile_cascade.detectMultiScale(gray, 1.1, 4)
            for (x, y, w, h) in faces:
                if show_Boxes:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

                roi_gray = gray[y:y + h, x:x + h]
                roi_color = img[y:y + h, x:x + h]
                #eyes = smile_cascade.detectMultiScale(gray, 2, 20)
                #smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=20)
                self.mouth = (int(x + (w/2)), int(y + (0.75 * h)))
                cv2.circle(img, self.mouth, 2, (255, 0, 0), 2)
                


                xpos = servo_xangle(self.mouth[0], 70)
                print(xpos, self.mouth[0])
                Servo1.goto(xpos)
                #print(ypos, self.mouth)
                #return self.mouth



            

            cv2.imshow("img", img)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break




#t = threading.Thread(target=cv)
#t.start()
#t.join()

ft = ft()



ft.cv()


#cap.release()
#cv2.destroyAllWindows()






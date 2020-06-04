import cv2
import numpy as np
import serial
import time
import sys
import controller


patrolStateX = 0
patrolStateY = 0


def patrol():
    global patrolStateX
    global patrolStateY
    
    if patrolStateX > 360:
        patrolStateX = 0

    if patrolStateX > 180:
        direction = -1
    else: 
        direction = 1

    patrolStateX += 1
    print(direction, patrolStateX)

    

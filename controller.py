import serial
import numpy as np
import serial
import time
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import gui
import threading


class Turret():

    def __init__(self, port, debug=False):
        self.serial = serial.Serial(port, 9600, timeout=5)
        self.debug = debug
    def gotoXY(self, xangle, yangle):
        self.serial.write(("X" + str(xangle) + "," + "Y" + str(yangle)).encode("utf-8"))
        
        if self.debug:
            print(("X" + str(xangle) + "," + "Y" + str(yangle)).encode("utf-8"))
            print("X" + str(xangle) + "," + "Y" + str(yangle))
        
    
    def gotoX(self, posx):
        
        self.serial.write(("X" + str(posx) + ",").encode("utf-8"))

        if self.debug: 
            print("went to: ", posx, )
        
    
    def gotoY(self, posy):
        self.serial.write(("Y" + str(posy)).encode("utf-8"))

        if self.debug:
            print("went to: ", posy, "   ", (("Y" + str(posy)).encode("utf-8")))
    
    def step(self, stepCount):
        self.serial.write(("S" + str(stepCount)).encode("utf-8"))

        if self.debug:
            print("stepped: ", stepCount)




def check_sliderX(self):
    x = self.horizontalSlider.sliderPosition()
    turret.gotoX(x)
    turret.step(4)


def check_sliderY(self):
    y = self.verticalSlider.sliderPosition()
    turret.gotoY(y)
    


class App(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        print(self.verticalSlider.sliderPosition())
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(180)
        self.verticalSlider.setMinimum(20)
        self.verticalSlider.setMaximum(170)
        #self.horizontalSlider.sliderMoved.connect(lambda: check_slider(self))
        self.verticalSlider.valueChanged.connect(lambda: check_sliderY(self))
        self.horizontalSlider.valueChanged.connect(lambda: check_sliderX(self))

def startgui():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = App()
    form.show()
    app.exec_()


if __name__ == "__main__":
    turret = Turret("COM6")
    startgui()
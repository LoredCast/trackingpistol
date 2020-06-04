import serial
from PyQt5 import QtCore, QtGui, QtWidgets
import gui
import time
import threading

serial = serial.Serial("COM6", 9800, timeout=1)

class Servo:
    def __init__(self, index):
        Servo.index = index

    def gotoX(self, posx):
        
        serial.write(("X" + str(posx) + ",").encode("utf-8"))
        time.sleep(0.005)
        print(posx)
        #print("Out:", serial.read(2).decode("utf-8"))
    
    def gotoY(self, posy):
        
        print(posy)
        serial.write(("Y" + str(posy)).encode("utf-8"))
        #print("Out:", serial.read(2).decode("utf-8"))

def output(chunk_size=1):

    read_buffer = b''

    while True:
        if serial.in_waiting:

        # Read in chunks. Each chunk will wait as long as specified by
        # timeout. Increase chunk_size to fail quicker
            byte_chunk = serial.read(size=chunk_size)
            read_buffer += byte_chunk
              	
            if byte_chunk == b"\n":
                print(read_buffer)
                read_buffer = b""
            
        
            
        

       

out = threading.Thread(target=output)
out.start()


Servo1 = Servo(1)

def check_sliderX(self):
    x = self.horizontalSlider.sliderPosition()
    Servo1.gotoX(x)
    
    #print((str(x) + "," + str(y)).encode("utf-8"))
    #print(chr(x).encode("utf-8"))


def check_sliderY(self):

    y = self.verticalSlider.sliderPosition()
    Servo1.gotoY(y)
    
    #print((str(x) + "," + str(y)).encode("utf-8"))
    #print(chr(y).encode("utf-8") + chr(180).encode("utf-8"))













class App(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        print(self.verticalSlider.sliderPosition())
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(180)
        self.verticalSlider.setMinimum(82)
        self.verticalSlider.setMaximum(110)
        #self.horizontalSlider.sliderMoved.connect(lambda: check_slider(self))
        self.verticalSlider.valueChanged.connect(lambda: check_sliderY(self))
        self.horizontalSlider.valueChanged.connect(lambda: check_sliderX(self))

def startgui():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = App()
    form.show()
    app.exec_()

startgui()

gui = threading.Thread(target=startgui)

gui.start()

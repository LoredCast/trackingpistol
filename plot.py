import cv2
import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication, QMainWindow, QGraphicsView, QGridLayout
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtGui import QImage, QPixmap
import pyqtgraph as pg
import Tracker
import controller

face_cascade = cv2.CascadeClassifier("venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")


mouth_xy = (0,0)


time = [0]
x = []
y = []

x_current = []
y_current = []


turret = controller.Turret("COM3")
current_angleX = 90
current_angleY = 90

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        global mouth_xy

        cap = cv2.VideoCapture(0)
        while True:
            
            ret, frame = cap.read()
            if ret:
                
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.2, 5, minSize=(13,13))
                for (x, y, w, h) in faces:
                    global current_angleX, current_angleY

                    if len(faces) == 1:
                        Tracker.trackX(mouth_xy[0])
                        Tracker.trackY(mouth_xy[1])

                        current_angleY += Tracker.pidY.output
                        current_angleX += Tracker.pidX.output
                        turret.gotoY(current_angleY)

            

                        turret.step(Tracker.pidX.output)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    mouth_xy = (int(x + (w/2)), int(y + (h/2)))
                    
                
                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)



class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    @pyqtSlot(QImage)
    def _update(self, image):
        global x, y, time, x_current, y_current, current_angleX, current_angleY
        
        
        
        
        self.label.setPixmap(QPixmap.fromImage(image))
        


        if len(x) > 200:
            x = x[1:]
        x.append(Tracker.pidX.target)

        if len(x_current) > 200:
            x_current = x_current[1:]
        x_current.append(current_angleY)

        
        if len(y_current) > 200:
            y_current = y_current[1:]
        y_current.append(current_angleY)
        
        if len(y) > 200:
            y = y[1:]
        y.append(Tracker.pidY.target)

        
        

        self.data_lineX.setData(x)
        self.data_lineXl.setData(x_current)
        self.data_lineYl.setData(y_current)
        self.data_lineY.setData(y)

    def initUI(self):

        self.plotlabel = QLabel(self)
        self.graphWidgetX = pg.PlotWidget()
        self.graphWidgetY = pg.PlotWidget()


        self.graphWidgetX.setTitle("X Axis")
        self.graphWidgetY.setTitle("Y Axis")

        self.graphWidgetX.setYRange(0, 180, padding=0)
        self.graphWidgetY.setYRange(0, 180, padding=0)

        self.data_lineX = self.graphWidgetX.plot(name="Measured")
        self.data_lineXl = self.graphWidgetX.plot(name="Live", pen=pg.mkPen('r'))
        self.data_lineY = self.graphWidgetY.plot(name="Measured")
        self.data_lineYl = self.graphWidgetY.plot(name="Live", pen=pg.mkPen('r'))
        

        layout = QGridLayout(self)
        layout.addWidget(self.graphWidgetX, 1,0)
        layout.addWidget(self.graphWidgetY, 1,1)
        self.plot = self.graphWidgetX.getPlotItem()
        self.setWindowTitle("Test")
        
        self.resize(1800, 1200)
        # create a label
        self.label = QLabel(self)
        self.label.move(1000, 10)
        self.label.resize(640, 480)
        layout.addWidget(self.label, 0,0)
        th = Thread(self)
        th.changePixmap.connect(self._update)
        th.start()

        
        
        self.show()




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = App()
    
    sys.exit(app.exec_())
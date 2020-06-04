import time
from matplotlib import pyplot as plt
import random


class pid:
    def __init__(self, p, i, d):
        self.p = p
        self.i = i
        self.d = d

    oldTime = 0
    dt = 0
    
    iVal = 0
    oldErr = 0
    newError = 0
    dE = 0
    output = 0
    def update(self, current, target):

        self.newErr = target - current
        self.dE = self.newErr - self.oldErr
        self.oldErr = self.newErr

        newTime = time.time()
        self.dt = (newTime - self.oldTime) if (self.oldTime != 0) else 0
        self.oldTime = newTime
        self.output = self.derivative() + self.proportional(self.newErr) + self.integral(self.newErr)
        print("Error ", self.newErr)

   
    def proportional(self, err):
        print(f"P {self.p * err}" )
        return self.p * err


    def integral(self, err):
        self.iVal += self.i * err * self.dt
        print("I ", self.iVal)
        return self.iVal
    
    def derivative(self):
        D = (self.d * (self.dE/self.dt)) if self.dt != 0 else 0
        print(self.dE)
        print("D ", D)
        return D
    
if __name__ == "__main__":
    values = []
    times = []

    p = pid(0.5, 0.4,0.001)
    current = 40
    for i in range(100):
        values.append(current)
        times.append(i * 0.01)
        current += p.output + (random.randint(1, 100) / 10) 
        p.update(current, 1000)
        print("current: ", current, "output: ", p.output)
        time.sleep(0.01)

        

    plt.plot(times, values)
    plt.show()
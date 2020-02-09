import serial
import time
import threading

class sensors:

    def __init__(self):
        
        self.temp = 0
        self.soil = 0
        
        self.ser = serial.Serial('COM8',9600)  #change ACM number as found from ls /dev/tty/ACM*
        self.ser.baudrate = 9600

        thread = threading.Thread(target=self.run, args=())
        thread.start()

    def run(self):
        while True:
            readSer = self.ser.read_until()
            readStr = readSer.decode()
            if "Temp" in readStr:
                self.temp = readStr[5:]
            elif "Soil" in readStr:
                self.soil = readStr[5:]


    def getTemp(self):
        return float(self.temp)
        
    def getSoil(self):
        return float(self.soil)

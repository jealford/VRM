import serial
import time

ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate=9600


def getTemp(str):
    temp = str[5:]
    return float(temp)
def getSoil(str):
    soil = str[5:]
    return float(soil)


while True:
    readSer=ser.readline()
    if "Temp" in readSer:
        print (getTemp(readSer))
    elif "Soil" in readSer:
        print (getSoil(readSer))
    time.sleep(.25)

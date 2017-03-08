# Rotate: flex (but not when arm is up) [EMG]
# Time threshold: 700 milliseconds
# Amplitude threshold: 0.15 millivolts

# Left/right: move arm left or right [accelerometer + gyro]
# Hard drop: raise arm up + flex [gyro + EMG]

import serial

import matplotlib.pyplot as plt                 # Import matplotlib module
from scipy import signal

microSec = []
rawADC = []
milliVolts = []
highPass = []
highLowPass = []
rectified = []
boxCar = []

startTime = 0
threshold_mV = 0.15
threshold_us = 700000


################################################################################
print "Please input name of data file: "
myFile = raw_input()
f = open(myFile, "r")

myLine = 1
while myLine:
    myLine = f.readline()
    myLine = myLine.split()
    print myLine
    for index in range(0, len(myLine)):
        microSec.append(float(myLine[0]))
        rawADC.append(float(myLine[1]))
        milliVolts.append(float(myLine[2]))
        highPass.append(float(myLine[3]))
        highLowPass.append(float(myLine[4]))
        rectified.append(float(myLine[5]))
        boxCar.append(float(myLine[6]))
		
		#Rotating a tetris block by flexing
		if((startTime == 0) || ((microSec.index(len(microSec)) - startTime) >= threshold_us)):
			if(boxCar.index(len(boxCar)-1) >= threshold):
				startTime = microSec.index(len(microSec)-1)
				
				#register rotation button here


################################################################################
plt.figure(1)
plt.subplot(2, 1, 1)
plt.plot(microSec, rawADC)
plt.title("Raw EMG Values")
plt.xlabel("Time (us)")
plt.ylabel("Raw EMG Values")

plt.subplot(2, 1, 2)
plt.plot(microSec, milliVolts)
plt.title("Millivolts")
plt.xlabel("Time (us)")
plt.ylabel("Voltage (mV)")

plt.figure(2)
plt.subplot(2, 1, 1)
plt.plot(microSec, highPass)
plt.title("HP Only")
plt.xlabel("Time (us)")
plt.ylabel("Voltage (mV)")

plt.subplot(2, 1, 2)
plt.plot(microSec, highLowPass)
plt.title("HP and LP")
plt.xlabel("Time (us)")
plt.ylabel("Voltage (mV)")

plt.figure(3)
plt.subplot(2, 1, 1)
plt.plot(microSec, rectified)
plt.title("Rectified")
plt.xlabel("Time (us)")
plt.ylabel("Voltage (mV)")

plt.subplot(2, 1, 2)
plt.plot(microSec, boxCar)
plt.title("Boxcar Filter")
plt.xlabel("Time (us)")
plt.ylabel("Voltage (mV)")

plt.show()

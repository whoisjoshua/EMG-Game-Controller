# Rotate: flex (but not when arm is up) [EMG]
# Time threshold: 700 milliseconds
# EMG threshold: 0.15 millivolts

# Left/right: move arm left or right [accelerometer + gyro]
# Gyro rest position: nothing, close to zero
# Gyro L: gy, neg to pos, magnitude 200+
# Gyro R: gy, pos to neg, magnitude 200+
# Accel threshold: magnitude >= 1.5

# Hard drop: raise arm up + flex [gyro + EMG]
# Gyro up position: gz, pos to neg, magnitude 200+
# EMG threshold: 0.15 millivolts

# Index 0: time, 1: filtered analog, 2-4: accelerometer, 5-7: gyroscope

import serial
import matplotlib.pyplot as plt                 # Import matplotlib module
from scipy import signal

microSec = []
milliVolts = []
boxCar = []
am = []
gy = []
gz = []

## Conversion constants ##
voltUnit = 3.3 / 1024
accelRange = 2
gyroRange = 250

startTime1 = 0
startTime2 = 0

#Rotation thresholds
threshold_mV = 0.15
threshold_rotate_us = 700000

#RL/Hard drop thresholds
threshold_gyro = 200 #Left (-) Right (+) for gy; Up (+) for gz
threshold_gyro_us = 800000 # Right/Left

## Function to convert raw analog values to V ##
def convertAnalog(nRaw):
    analogScaled = int(nRaw) * voltUnit
    return analogScaled

## Function to convert raw accelerometer values to g ##
def convertAccel(aRaw):
    accelScaled = ((int(aRaw) / 32768.0) * accelRange)
    return accelScaled

## Function to convert raw gyroscope values to */s ##
def convertGyro(gRaw):
    gyroScaled = (int(gRaw) / 32768.9) * gyroRange
    return gyroScaled

## Function to convert microseconds to milliseconds $$
def convertTime(microS):
    timeScaled = microS * 0.001
    return timeScaled

################################################################################
print "Please input name of data file: "
myFile = raw_input()
f = open(myFile, "w")

ser = serial.Serial("/dev/cu.usbmodem1411")     # Open serial port


while(1):
    myLine = ser.readline()
    myLine = myLine.split()
    #print myLine

    for index in range(0, len(myLine)):
        microSec.append(float(myLine[0]))
        # f.write(myLine[0])
        # f.write(" ")

        boxCar.append(float(myLine[1]))
        # f.write(myLine[1])
        # f.write(" ")

        ax = convertAccel(myLine[2])
        ay = convertAccel(myLine[3])
        az = convertAccel(myLine[4])
        am.append((ax**2 + ay**2 + az**2)**(0.5))
        # f.write(str((ax**2 + ay**2 + az**2)**(0.5)))
        # f.write(" ")

        gy.append(convertGyro(myLine[6]))
        # f.write(str(convertGyro(myLine[6])))
        # f.write(" ")

        gz.append(convertGyro(myLine[7]))
        # f.write(str(convertGyro(myLine[7])))
        # f.write("\n")

        #Checking if time of threshold has passed for rotation time threshold
        if((startTime1 == 0) or ((microSec[-1] - startTime1) >= threshold_rotate_us)):
            #Rotating a tetris block by flexing
            # print(boxCar[-1])
            if(boxCar[-1] >= threshold_mV):
                startTime1 = microSec[-1]
                #register rotation button here
                #Serial.write("U")
                print("U")

        #Checking if time of threshold has passed for gyro time threshold
        if((startTime2 == 0) or (microSec[-1] - startTime2) >= threshold_gyro_us):
            #Left/Right/Up
            if((abs(gy[-1]) >= threshold_gyro) or gz[-1] >= threshold_gyro):
                startTime2 = microSec[-1]

                #register left by checking if negative gy
                if(gy[-1] < threshold_gyro*(-1)):
                    #register left button here
                    #Serial.write("L")
                    print("L")

                #register right by checking if positive gy
                if(gy[-1] > threshold_gyro):
                    #register right button here
                    #Serial.write("R")
                    print("R")

                #register hard drop by checking if positive gz
                if(gz[-1] > threshold_gyro):
                    #register hard drop
                    print("B")

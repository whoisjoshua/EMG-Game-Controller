import matplotlib.pyplot as plt                 # Import matplotlib module

time = []
# boxCar = []
# am = []
# gx = []
gy = []
gz = []

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
        time.append(float(myLine[0]))
        # gx.append(float(myLine[1]))
        gy.append(float(myLine[3]))
        gz.append(float(myLine[4]))

################################################################################
plt.figure(1)
# plt.subplot(3, 1, 1)
# plt.plot(time, gx)
# plt.title("gx")
# plt.xlabel("Time (us)")
# plt.ylabel("gx")

plt.subplot(2, 1, 1)
plt.plot(time, gy)
plt.title("gy")
plt.xlabel("Time (us)")
plt.ylabel("gy")

plt.subplot(2, 1, 2)
plt.plot(time, gz)
plt.title("gz")
plt.xlabel("Time (us)")
plt.ylabel("gz")

plt.show()

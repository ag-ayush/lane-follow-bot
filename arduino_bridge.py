import serial

def sendToArduino(sendStr):
    ser.write(sendStr)


def recvFromArduino():
    global startMarker, endMarker

    ck = ""
    x = " "
    byteCount = -1  # to allow for the fact that the last increment will be one too many

    # wait for the start character
    while ord(x) != startMarker:
        x = ser.read()

    # save data until the end marker is found
    while ord(x) != endMarker:
        if ord(x) != startMarker:
            ck = ck + x
            byteCount += 1
        x = ser.read()

    return (ck)


def waitForArduino():
    # wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
    # it also ensures that any bytes left over from a previous message are discarded

    global startMarker, endMarker

    msg = ""
    while msg.find("Arduino is ready") == -1:

        while ser.inWaiting() == 0:
            pass

        msg = recvFromArduino()

        print msg
        print


def runTest(td):
    numLoops = len(td)
    waitingForReply = False

    n = 0
    while n < numLoops:

        teststr = td[n]

        if waitingForReply:

            while ser.inWaiting() == 0:
                pass

            dataRecvd = recvFromArduino()
            print "Reply Received  " + dataRecvd
            n += 1
            waitingForReply = False

            print "==========="
        else:
            sendToArduino(teststr)
            print "Sent from PC -- LOOP NUM " + str(n) + " TEST STR " + teststr
            waitingForReply = True

        # time.sleep(5)   # Pauses in between, else it would be looping

import random

def send_data(floater):
    waitingForReply = False

    if floater < -0.1:
        data = ("<LEFT," + str(abs(floater)) + ">")
    elif floater > 0.1:
        data = ("<RIGHT," + str(abs(floater)) + ">")
    else:
        data = ("<STRAIGHT, 0>")
    for n in range(2):
        if waitingForReply:
            while ser.inWaiting() == 0:
                pass
            dataRecvd = recvFromArduino()
            print "Reply Received  " + dataRecvd
            waitingForReply = False
            print "==========="
        else:
            sendToArduino(data)
            print "Sent from PC -- LOOP NUM " + str(n) + " TEST STR " + data
            waitingForReply = True


serPort = "/dev/ttyACM0"
baudRate = 9600
ser = serial.Serial(serPort, baudRate)
print "Serial port " + serPort + " opened  Baudrate " + str(baudRate)

startMarker = 60    # ord('<')
endMarker = 62      # ord('>')

waitForArduino()

testData = []
for n in range(100):
    testData.append(random.uniform(-1, 1))

printData = []
testData.sort()
for data in testData:
    if data < -0.1:
        printData.append("<LEFT," + str(abs(data)) + ">")
    elif data > 0.1:
        printData.append("<RIGHT," + str(abs(data)) + ">")
    else:
        printData.append("<STRAIGHT, 0>")

printData.append("<STRAIGHT, 0>")

ser.close
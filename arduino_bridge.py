import serial

serPort = "/dev/ttyACM0"
baudRate = 9600
ser = serial.Serial(serPort, baudRate)

print "Serial port " + serPort + " opened  Baudrate " + str(baudRate)

def close():
    ser.close

def send_data(floater):

    if floater < -0.1:
        data = ("<LEFT," + str(abs(floater)) + ">")
    elif floater > 0.1:
        data = ("<RIGHT," + str(abs(floater)) + ">")
    else:
        data = ("<STRAIGHT, 0>")
    ser.write(data)
    print "Sent from PC -- LOOP NUM TEST STR " + data

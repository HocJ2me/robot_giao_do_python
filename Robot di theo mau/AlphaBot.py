import RPi.GPIO as GPIO
import time
import serial
time.sleep(3)

ser = serial.Serial(
    port = '/dev/ttyACM0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)
class AlphaBot(object):

    def __init__(self):
        pass
    def forward(self):
        ser.write(b"1")
        ser.flush()
    def backward(self):
        ser.write(b"2")
        ser.flush()
    def right(self):
        ser.write(b"3")
        ser.flush()
    def left(self):
        ser.write(b"4")
        ser.flush()
    def stop(self):
        ser.write(b"5")
        ser.flush()
    def close(self):
        ser.close()

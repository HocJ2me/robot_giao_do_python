import RPi.GPIO as GPIO
import time
import serial

class AlphaBot(object):
    
    def __init__(self):
        ser = serial.Serial(
            port = '/dev/ttyAMA0',
            baudrate = 9600,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = 1
        )
    def forward(self):
        ser.print("1")
        ser.flush()
    def backward(self):
        ser.print("2")
        ser.flush()
    def right(self):
        ser.print("3")
        ser.flush()
    def left(self):
        ser.print("4")
        ser.flush()
    def stop(self):
        ser.print("5")
        ser.flush()

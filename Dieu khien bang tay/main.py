#!/usr/bin/python
# -*- coding:utf-8 -*-
from bottle import get,post,run,route,request,template,static_file
from AlphaBot import AlphaBot
import threading
import socket #ip
import os,sys
import RPi.GPIO as GPIO
import time
car = AlphaBot()
@get("/")
def index():
    return template("index1")
    
@route('/<filename>')
def server_static(filename):
    return static_file(filename, root='./')

@route('/fonts/<filename>')
def server_fonts(filename):
    return static_file(filename, root='./fonts/')
    
@post("/cmd")
def cmd():
    code = request.body.read().decode()
    speed = request.POST.get('speed')
    if(speed != None):
#        car.setPWMA(float(speed))
#        car.setPWMB(float(speed))
        print(speed)
    if code == "stop":
        car.stop()
        print("stop")
    elif code == "forward":
        car.forward()
        print("forward")
    elif code == "backward":
        car.backward()
        print("backward")
    elif code == "turnleft":
        car.left()
        print("turnleft")
    elif code == "turnright":
        car.right()
        print("turnright")
    elif code == "pumpOn":
        car.pumpOn()
        print("pumpOn")
    elif code == "pumpOff":
        car.pumpOff()
        print("pumpOff")
    else:
        value = 0
        try:
            value = int(speed)
            if(value >= 0 and value <= 100):
                print(value)
  #              car.setPWMA(value)
  #              car.setPWMB(value)
        except:
            print("Command error")
    return "OK"

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect(('8.8.8.8',80))
localhost=s.getsockname()[0]
run(host = localhost, port = 8001)

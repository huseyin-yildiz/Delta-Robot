# -*- coding: utf-8 -*-
"""
Ub = 346.600; Ua = 20.450; 
  Wb = 142.5; 
  Wa = 142.5; 
  L = 390;
 
  
  d1 = Ub * cos(30);
  d2 = Ua * cos(30);
  d4 = Ua * sin(30);
  d3 = Ub * sin(30);
  
%   q1 = zp + sqrt((L ^ 2) - ((-d1 + xp - d2) ^ 2) - ((d3 + yp + d4) ^ 2));
%   
%   q2 = zp + sqrt((L ^ 2) - ((d1 + xp + d2) ^ 2) - ((-d3 + yp - d4) ^ 2));
%   
%   q3 = zp + sqrt((L ^ 2) - ((xp) ^ 2) - ((Ub + yp - Ua) ^ 2));
  
  q1 = zp + sqrt((L ^ 2) - ((-d1 + xp + d2) ^ 2) - ((d3 + yp - d4) ^ 2))
  
  q2 = zp + sqrt((L ^ 2) - ((d1 + xp - d2) ^ 2) - ((d3 + yp - d4) ^ 2))
  
  q3 = zp + sqrt((L ^ 2) - ((xp) ^ 2) - ((Ub + yp - Ua) ^ 2))


q1 = q1 - 2.138368010890548e+02
q2 = q2 - 2.138368010890548e+02
q3 = q3 - 2.138368010890548e+02

"""
import math
from time import sleep
import RPi.GPIO as GPIO

Ub = 346.600
Ua = 20.450
Wb = 142.5
Wa = 142.5
L = 390
 

d1 = Ub * math.cos(30)
d2 = Ua * math.cos(30)
d4 = Ua * math.sin(30)
d3 = Ub * math.sin(30)

q1 = math.zp + math.sqrt((L ^ 2) - ((-d1 + math.xp + d2) ^ 2) - ((d3 + math.yp - d4) ^ 2))

q2 = math.zp + math.sqrt((L ^ 2) - ((d1 + math.xp - d2) ^ 2) - ((d3 + math.yp - d4) ^ 2))

q3 = math.zp + math.sqrt((L ^ 2) - ((math.xp) ^ 2) - ((Ub + math.yp - Ua) ^ 2))

R=  2*math.pi*3*0.1125/360

step = (q1 / R)



DIR = 20
STEP = 21
CW = 1
CCW = 0
SPR = step



GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR,GPIO.OUT)
GPIO.setup(STEP,GPIO.OUT)
GPIO.output(DIR,CW)

step_count = SPR
delay=0.0208

for x in range(step_count):
    GPIO.output(STEP,GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP,GPIO.LOW)
    sleep(delay)

sleep(0.5)
GPIO.output(DIR,CCW)
for x in range(step_count):
    GPIO.output(STEP,GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP,GPIO.LOW)
    sleep(delay)


















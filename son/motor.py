import RPi.GPIO as GPIO


input1 = 21

def motor_calistir():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(input1,GPIO.OUT)
    GPIO.output(input1,GPIO.HIGH)

def motor_durdur():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(input1,GPIO.OUT)
    GPIO.output(input1,GPIO.LOW)
# Motor çalıştırma

input1 = 24
en = 18 

def motor_calistir():
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(input1,GPIO.OUT)
    GPIO.setup(en,GPIO.OUT)
    GPIO.output(input1,GPIO.HIGHT)
    p=GPIO.PWM(en,1000)
    p.start(50)

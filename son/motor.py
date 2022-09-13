import RPi.GPIO as GPIO

input1 = 18 

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
    






# Stap motorları çalıştıran fonksiyon
def step_motor(start,S_count):
    for z in range(int(S_count)):
        GPIO.output(start,GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(start,GPIO.LOW)
        time.sleep(delay)
        print(z)
    print("bitti...")
    
    
# step motların doğru çalışması için gerekli olan ayarlamalar
def step_motor_1():
    if step<0:
        CW = 0
        GPIO.output(DIR,CW)
        step_motor(STEP_pin,step_count)
        
       
    elif step>0:
        CW = 1
        GPIO.output(DIR,CW)
        step_motor(STEP_pin,step_count)
        
    else:
        pass



def step_motor_2():    
    if step1<0:
        CW = 0
        GPIO.output(DIR_1,CW)
        step_motor(STEP1_pin,step_count_1)

    elif step1>0:
        CW = 1
        GPIO.output(DIR_1,CW)
        step_motor(STEP1_pin,step_count_1)
     
    else:
        pass
    
    
def step_motor_3():
    
    if step2<0:
        CW = 0
        GPIO.output(DIR_2,CW)
        step_motor(STEP2_pin,step_count_2)

        
    elif step2>0:
        CW = 1
        GPIO.output(DIR_2,CW)
        step_motor(STEP2_pin,step_count_2)
    else:
        pass

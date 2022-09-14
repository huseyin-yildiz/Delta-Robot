from goruntu_isleme import *
import goruntu_isleme
from haberlesme import *
from motor import *


from threading import Thread


# ! bant köşe noktaları kalibre için get_bant_corners() kullan
#corner_points = [(0, 24), (804, 192), (0, 199), (804, 13)] #get_bant_corners(cap)

# print(corner)

global serial
serial = connect('/dev/ttyUSB0',9600)


command = 't6.txt="'+str(5)+'"' 
write_cmd(serial,command)



func = None
color = None
cmd = None

goruntu_isleme.count = 0 

while(True):
    cmd_new = serial.read()
    if(cmd_new):
        cmd = cmd_new
    if(cmd):
            
        if(cmd == CMD_SAYMA_S):
            print("ss")
            func = renk_say
            color = COLOR_YELLOW
            
        elif(cmd == CMD_SAYMA_M):
            print("sm")
            func = renk_say
            color = COLOR_BLUE
            
        elif(cmd == CMD_TAKIP_S): 
            print("ts")
            func = renk_takip
            color = COLOR_YELLOW
            
            
        elif(cmd == CMD_TAKIP_M):
            print("tm")
            func = renk_takip
            color = COLOR_BLUE
            
        elif(cmd == CMD_AYIKLA_S):
            print("as")
            func = renk_ayirma
            color = COLOR_BLUE
            
            
        elif(cmd == CMD_AYIKLA_M):
            print("am")
            func = renk_ayirma
            color = COLOR_BLUE
            
        elif(cmd == CMD_BACK):
            print("back")
            func = None
            color = None
            goruntu_isleme.count = 0 
            motor_durdur()
        
        if(func):
            func(serial,color)
            motor_calistir()
        
        if cv2.waitKey(1) & 0xFF == ord("q"): 
            motor_durdur()
            break

 

# 
# 
# func = NONE
# color = CMD_NONE
# last_cmd = CMD_NONE
# thr = NONE
# stop = False 
# while True: 
#     cmd = read_cmd(ser)
#     
#     if cmd == CMD_NONE:
#         cmd = last_cmd
#     
#     if cmd == CMD_AYIRMA:
#         func = renk_ayirma
#         last_cmd = cmd
#         
#         
# 
#     elif cmd == CMD_SAYMA:
#         func = renk_say
#         last_cmd = cmd
#         if(color != CMD_NONE):
#             stop = False
#             thr = Thread(target=func,args=(color))
#             thr.start()
#             
#         
#             
#     elif cmd == CMD_TAKIP:
#         func = renk_takip
#         last_cmd = cmd
#         if(color != CMD_NONE and thr == NONE):
#             stop = False
#             thr = Thread(target=func,args=(color))
#             thr.start()
#             
#             
#             
#     elif cmd == CMD_SARI or cmd == CMD_MAVI:
#         color = cmd
#         stop = False
#         thr = Thread(target=func,args=(color))
#         thr.start()
#         motor_calistir()
#     
#     elif(cmd == CMD_CIKIS_1 or cmd == CMD_CIKIS_2 or cmd == CMD_CIKIS_3):
#         color = CMD_NONE
#         func = NONE
#         last_cmd = CMD_NONE
#         motor_durdur()
#         cmd = CMD_NONE
#         stop = True
# 





    #else:
     #   raise Exception("Yanlis komut geldi (renk komutu simdi gelmemeli)")
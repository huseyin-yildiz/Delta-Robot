from goruntu_isleme import *
from haberlesme import *
from motor import motor_calistir
from motor import motor_durdur

from threading import Thread




ser = connect('/dev/ttyUSB0',9600)



func = None
color = None
cmd = None
while(True):
    cmd_new = ser.read()
    if(cmd_new):
        cmd = cmd_new
    
    if(cmd):
            
        if(cmd == CMD_SAYMA_S):
            print("ss")
            func = renk_say
            color = COLOR_SARI
            
        elif(cmd == CMD_SAYMA_M):
            print("sm")
            func = renk_say
            color = COLOR_MAVI
            
        elif(cmd == CMD_TAKIP_S):
            print("ts")
            func = renk_takip
            color = COLOR_SARI
            
            
        elif(cmd == CMD_TAKIP_M):
            print("tm")
            func = renk_takip
            color = COLOR_MAVI
            
        elif(cmd == CMD_AYIKLA_S):
            print("as")
            func = renk_ayirma
            color = COLOR_MAVI
            
            
        elif(cmd == CMD_AYIKLA_M):
            print("am")
            func = renk_ayirma
            color = COLOR_MAVI
            
        elif(cmd == CMD_BACK):
            print("back")
            func = None
            color = None
            motor_durdur()
        
        if(func):
            func(color)
            motor_calistir()
        



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
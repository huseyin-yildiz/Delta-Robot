from haberlesme import *
import struct


ser = connect('/dev/ttyUSB0',9600)

# # ser.write(b'\xff')
# 
# #
# command = 't6.txt="'+str(6)+'"' 
# write_cmd(command)
# # k=struct.pack('B', 0xFF)
# # 
# #command = 't6.txt="'+str(2)+'"'
# #ser.write(command.encode())
# #ser.write(CMD_CLOSE)
# # 
# print(command)
# 
# 
# 
# '''
# 
# 
# command = 't6.txt="'+str(5)+'"' 
# ser.write(command.encode())
# ser.write(b'0xFF')
# ser.write(b'0xFF')
# ser.write(b'0xFF')
# '''

func = NONE
color = 
cmd = NONE
while(True):
    cmd = ser.read()
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
            func = NONE
            color = NONE
            
        func(color)       
        

        
        
from son.goruntu_isleme import *
from son.haberlesme import *
from son.motor import motor_calistir


motor_calistir()


last_cmd = CMD_NONE
while True: 
    cmd = read_cmd()
    
    if cmd == CMD_NONE:
        cmd = last_cmd
    elif cmd == CMD_AYIRMA:
        renk_ayırma()

    elif cmd == CMD_SAYMA:
        renk = read_cmd()
        renk_say(renk)
    
    elif cmd == CMD_TAKIP:
        renk_takip()

    else:
        raise Exception("Yanlis komut geldi (renk komutu simdi gelmemeli)")
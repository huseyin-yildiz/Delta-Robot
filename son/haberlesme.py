#%%
from pickle import NONE
import serial.tools.list_ports

CMD_NONE = b''
CMD_SAYMA =
CMD_AYIRMA =
CMD_TAKIP =
CMD_SARI = 
CMD_MAVI =

ser = NONE

def connect():
    ser = serial.Serial(port='/dev/ttyUSB0',
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1)


def read_cmd():
    if(ser == NONE):
        raise Exception("Raspberry ile baglanti yok. connect() yapmayı unutmayiniz")
    return ser.readline()

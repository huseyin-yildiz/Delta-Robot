#%%
from pickle import NONE
import serial.tools.list_ports

CMD_NONE = b''
CMD_SAYMA_S = b'\xa0'
CMD_SAYMA_M = b'\xa1'

CMD_TAKIP_S = b'\xb0'
CMD_TAKIP_M = b'\xb1'

CMD_AYIKLA_S = b'\xc0'
CMD_AYIKLA_M = b'\xc1'

CMD_CLOSE = b'\xff\xff\xff'

CMD_BACK = b'\xe0'


def connect(_port,_baud_rate):
    return serial.Serial(port=_port,
                    baudrate=_baud_rate,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=0)


def read_cmd(ser):
    if(ser == NONE):
        raise Exception("Nextion ile baglanti yok. connect() yapmayı unutmayiniz")
    return ser.readline()

ser = connect('/dev/ttyUSB0',9600)
def write_cmd(text):
    ser.write(text.encode())
    ser.write(CMD_CLOSE)


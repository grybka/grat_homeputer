from __future__ import absolute_import

from dripline.core import Provider, exceptions, fancy_doc
import board
import busio
from digitalio import DigitalInOut, Direction
try:
    import struct
except ImportError:
    import ustruct as struct
import serial

class PM25Spime(Spime):
    def __init__(self,**kwargs):
        Spime.__init__(self,**kwargs)

    def on_get(self):
        #I suppose I'll have it reconnect on every get.  Seems a little excessive
        uart=serial.Serial("/dev/ttyS0",baudrate=9600,timeout=3000)
        data=uart.read(32)
        data=list(data)
        buffer=data
        if len(buffer)<32:
            print("error, didnt get 32 bytes of data, got {}".format(len(buffer)))
            raise exceptions.DriplineHardwareError('error, didnt get 32 bytes of data')
            return []
        while buffer and buffer[0] != 0x4d:
            buffer.pop(0)
        frame_len=struct.unpack(">H",bytes(buffer[2:4]))[0]
        if frame_len != 28:
            print("error, frame length not right")
            raise exceptions.DriplineHardwareError('error, frame length not right')
            return []
        frame = struct.unpack(">HHHHHHHHHHHHHH", bytes(buffer[4:]))
        pm10_standard, pm25_standard, pm100_standard, pm10_env, \
            pm25_env, pm100_env, particles_03um, particles_05um, particles_10um, \
            particles_25um, particles_50um, particles_100um, skip, checksum = frame

        check = sum(buffer[0:30])
        if check != checksum:
            print("checksum failed")
            raise exceptions.DriplineHardwareError('error, checksum failed')
            return []
        return [particles_03um,particles_05um,particles_10um,particles_25um,particles_50um,particles_100um]
    
__all__.append('PM25Spime')

    

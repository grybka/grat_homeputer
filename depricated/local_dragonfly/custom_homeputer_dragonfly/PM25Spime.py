from __future__ import absolute_import

from dripline.core import Provider, exceptions, fancy_doc, Spime
import board
import busio
from digitalio import DigitalInOut, Direction
import serial
try:
    import struct
except ImportError:
    import ustruct as struct

import logging
logger = logging.getLogger(__name__)

__all__ = []

class PM25Spime(Spime):
    def __init__(self,**kwargs):
        print("p25 init called")
        Spime.__init__(self,**kwargs)

    def on_get(self):
        #I suppose I'll have it reconnect on every get.  Seems a little excessive
        print("connecting to serial")
        #led = DigitalInOut(board.D13)
        #led.direction = Direction.OUTPUT
        uart=serial.Serial("/dev/ttyS0",baudrate=9600,timeout=3000)
        for cycle in range(100):
            print("reading some data")
            buffer = []
            data=uart.read(32)
            data=list(data)
            buffer+=data
            print("buffer length now {}".format(len(buffer)))
            while buffer and buffer[0] != 0x42:
                buffer.pop(0)
            if len(buffer) > 200:
                buffer = []  # avoid an overrun if all bad data
            if len(buffer) < 32:
                continue
            if buffer[1] != 0x4d:
                buffer.pop(0)
                continue
            #raise exceptions.DriplineHardwareError('error, didnt get 32 bytes of data')
            frame_len=struct.unpack(">H",bytes(buffer[2:4]))[0]
            if frame_len != 28:
                buffer =[]
                continue
            frame = struct.unpack(">HHHHHHHHHHHHHH", bytes(buffer[4:]))
            pm10_standard, pm25_standard, pm100_standard, pm10_env, \
                pm25_env, pm100_env, particles_03um, particles_05um, particles_10um, \
                particles_25um, particles_50um, particles_100um, skip, checksum = frame

            check = sum(buffer[0:30])
            if check != checksum:
                print("checksum failed")
                raise exceptions.DriplineHardwareError('error, checksum failed')
                return []
            return {"pm2_5": pm25_env,"pm_10":pm10_env,"pm_100":pm100_env}
            #return [pm10_env,pm25_env,pm100_env,particles_03um,particles_05um,particles_10um,particles_25um,particles_50um,particles_100um]
        raise exceptions.DriplineHardwareError('communication to pm25 sensor failed somehow')
    
__all__.append('PM25Spime')

    

import serial
import struct
import time
from requests import post

def read_pm25():
    response_object={"error": []}
    try:
        uart=serial.Serial("/dev/ttyS0",baudrate=9600,timeout=3)
    except serial.SerialException as err:
        print("reporting serial exception {}".format(err))
        response_object["error"].append("failed to connect serial: {}".format(err))
        return response_object
    for attempt in range(5):
        print("reading...")
        data = uart.read(32)  # read up to 32 bytes
        data = list(data)
        print("read: ", len(data))          # this is a bytearray type

        buffer += data

        while buffer and buffer[0] != 0x42:
            buffer.pop(0)

        if len(buffer) > 200:
            buffer = []  # avoid an overrun if all bad data
        if len(buffer) < 32:
            continue

        if buffer[1] != 0x4d:
            buffer.pop(0)
            continue

        frame_len = struct.unpack(">H", bytes(buffer[2:4]))[0]
        if frame_len != 28:
            buffer = []
            continue

        frame = struct.unpack(">HHHHHHHHHHHHHH", bytes(buffer[4:]))

        pm10_standard, pm25_standard, pm100_standard, pm10_env, \
            pm25_env, pm100_env, particles_03um, particles_05um, particles_10um, \
            particles_25um, particles_50um, particles_100um, skip, checksum = frame

        check = sum(buffer[0:30])

        if check != checksum:
            buffer = []
            continue
        response_object["pm2.5"]=pm25_env
        response_object["pm10"]=pm10_env
        response_object["pm100"]=pm100_env
        uart.close()
        return response_object
    uart.close()
    response_object["error"].append("out of retries")
    return response_object

def update_sensor(host,sensorname,value):
    url=host+"/api/states/sensor."+sensorname
    headers={'Authorization': 'Bearer ADBD', 'Content-Type': 'application/json'}
    payload={"state": str(value)}
    resquests.post(url,data=payload,headers=headers)
#c.setopt(pycurl.URL,url)
#    c.setopt(pycurl.POSTFIELDS,postfields)
#    c.setopt(pycurl.HTTPHEADER,["Authorization: Bearer ADBD","Content-Type: application/json"] )
#    c=pycurl.Curl()
#    c.perform()
#    c.close()

#initialization
while True:
    #attempt to read sensor
    data=read_pm25()
    if len(data["error"])!=0:
        continue
    #send if data is good
    update_sensor("10.0.0.3:8123","kitchen_pm25",data["pm2.5"])
    #wait appropriate amount of time
    time.sleep(30)

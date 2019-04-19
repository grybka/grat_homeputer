import serial
import struct
import time
import yaml
from requests import post

access_token=""

def read_pm25():
    response_object={"error": []}
    buffer=[]
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
        print("buffer length {}".format(len(buffer)))
        frame = struct.unpack(">HHHHHHHHHHHHHH", bytes(buffer[4:32]))

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

def update_sensor(host,sensorname,value,units):
    url=host+"/api/states/sensor."+sensorname
    headers={'Authorization': 'Bearer '+access_token, 'Content-Type': 'application/json'}
    payload={"state": str(value),"attributes": {"unit_of_measurement": units}}
    try:
        r=post(url,json=payload,headers=headers)
        print("request response was {}".format(r.text))
    except Exception as x:
        print("failed to post with error {}".format(x))

#initialization
authfile=open("./grat_auth.yaml")
authyaml=yaml.load(authfile,Loader=yaml.Loader)
authfile.close()
access_token=authyaml["ha_access_token"]

try:
    while True:
        #attempt to read sensor
        data=read_pm25()
        if len(data["error"])!=0:
            continue
        #send if data is good
        update_sensor("http://10.0.0.3:8123","kitchen_pm2_5",data["pm2.5"],"ug/m3")
        update_sensor("http://10.0.0.3:8123","kitchen_pm10",data["pm10"],"ug/m3")
        update_sensor("http://10.0.0.3:8123","kitchen_pm100",data["pm100"],"ug/m3")
        #wait appropriate amount of time
        time.sleep(30)
except KeyboardInterrupt:
    print("quitting")
    pass

# flask_web/app.py

from flask import Flask
import yaml
import serial
import struct
app = Flask(__name__)

@app.route('/pm25')
def hello_world():
    print("starting pm25")
    response_object={"error": []}
    try:
        uart=serial.Serial("/dev/ttyS0",baudrate=9600,timeout=3)
    except serial.SerialException as err:
        print("reporting serial exception {}".format(err))
        response_object["error"].append("failed to connect serial: {}".format(err))
        return yaml.dump(response_object,Dumper=yaml.Dumper)

    buffer=[]
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
        return yaml.dump(response_object,Dumper=yaml.Dumper)
    uart.close()
    response_object["error"].append("out of retries")
    return yaml.dump(response_object,Dumper=yaml.Dumper)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

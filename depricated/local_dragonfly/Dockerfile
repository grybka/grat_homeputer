FROM python:3.5

ADD ./dripline-python /dripline-python
COPY ./dragonfly /dragonfly
RUN pip install RPI.GPIO adafruit-blinka 
RUN pip install numpy
RUN pip install /dripline-python
RUN pip install /dragonfly[colorlog,database]
RUN pip install pyserial
RUN ln -s /etc/p8-auths/.project8_authentications.json /root/.project8_authentications.json



FROM python:3.5

ADD ./dripline-python /dripline-python
COPY ./dragonfly /dragonfly
RUN pip install /dripline-python
RUN pip install /dragonfly[colorlog,database]
RUN pip install RPI.GPIO
RUN pip install adafruit-blinka



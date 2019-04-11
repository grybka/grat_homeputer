FROM python:3

ADD ./dripline-python /dripline-python
COPY ./dragonfly /dragonfly
RUN pip install /dripline-python
RUN pip install /dragonfly[colorlog,database]


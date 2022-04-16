FROM python:3.6.7

ARG PINGPONG_ROOT=/ping-pong

COPY ./config ${PINGPONG_ROOT}/config
COPY ./referee ${PINGPONG_ROOT}/referee
COPY ./common ${PINGPONG_ROOT}/common
COPY ./requirements.txt ${PINGPONG_ROOT}/requirements.txt

RUN pip3 install -r ${PINGPONG_ROOT}/requirements.txt

WORKDIR ${PINGPONG_ROOT}
ENV FLASK_APP referee/service
ENV PYTHONPATH .

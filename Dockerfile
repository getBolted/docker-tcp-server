FROM debian:latest

RUN apt-get update -y \ 
    && apt-get install git software-properties-common python3.7 python3-pip -y

WORKDIR /home/workdir

RUN apt-get install python3-numpy python3-scipy python3-pandas -y

RUN pip3 install requests

COPY . /home/workdir

EXPOSE 32000
FROM ubuntu:xenial
MAINTAINER Peter Uhlenbruck
ADD . /app
WORKDIR /app
RUN apt-get update && apt-get -y upgrade && apt-get install -y python3.5-minimal python3-pip libssl-dev \
&& pip3 install -r requirements.txt \
&& apt-get purge -y python3-pip libssl-dev && apt-get autoremove -y --purge && apt-get clean \
&& rm -rf /var/lib/apt/*
EXPOSE 5000
CMD ["python3.5", "/app/run.py"]

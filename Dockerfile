FROM python:3.5.1
MAINTAINER Peter Uhlenbruck
ADD . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["python3.5", "run.py"]

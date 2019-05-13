FROM python:3.7-alpine
COPY . /usr/src/DistributedFlask
WORKDIR /usr/src/DistributedFlask
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

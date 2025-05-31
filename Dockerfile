# syntax=docker/dockerfile:1

FROM python:3.13-bookworm

EXPOSE 8080
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt update && apt -y install nodejs npm 
RUN npm install -g http-server

CMD ["http-server","-c-1"]

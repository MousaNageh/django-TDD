FROM python:3.7-alpine

WORKDIR /app 

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app


EXPOSE 8000
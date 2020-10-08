FROM python:3.8-slim-buster

COPY ./requirements.txt /app/requirements.txt 
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

WORKDIR /app

COPY . /app

EXPOSE 8000

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app

ARG VERSION
ENV VERSION=${VERSION}
ENV JWT_DEFAULT_REALM test

ENV BIND_HOST 0.0.0.0
ENV BIND_PORT 8000
ENV WORKERS 5

ENTRYPOINT ["bash", "entrypoint.sh"]
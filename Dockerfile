FROM python:alpine

WORKDIR /usr/app

RUN pip install redis

COPY server.py ./

#just for inner test
COPY client.py ./


CMD ["python", "server.py"]

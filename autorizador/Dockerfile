FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

COPY ./requirements.txt /autorizador/requirements.txt

WORKDIR /autorizador

RUN pip3 install pika && \
    pip3 install docker && \
    pip3 install -r requirements.txt

COPY . /autorizador

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]

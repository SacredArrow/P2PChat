FROM alpine:3.11

RUN apk add python3-tkinter python3
RUN apk add build-base
RUN apk add python3-dev
RUN apk add linux-headers

RUN pip3 install --upgrade pip
RUN pip3 install grpcio
RUN pip3 install grpcio-tools

COPY ./ /chat/

ENTRYPOINT python3 ./chat/server.py 6061 6062

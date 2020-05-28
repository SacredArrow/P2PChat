# P2PChat

## Prerequisites
- Python 3
- grpc
- tkinter

## Preparation

Generate files with ``python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. passing.proto``

## Usage

Run with ``python main.py <port1> <ip> <port2>``.  
Example: ``python3 main.py 6061 localhost 6062``.

## Docker
Build with ``docker build -t chad-ubuntu -f dockerfile-ubuntu``.  
Run with ``docker run -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -p <your_port>:6061 <image name> <ip> <peer_port>``, where ``ip`` is your host ip from ``sudo ip addr show docker0``. You might need to run ``xhost +"local:docker@"`` beforehand.

# Made by
- Кутленков Дмитрий  
- Чернявский Олег
- Келим Илья
- Сергеев Егор

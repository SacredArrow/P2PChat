# P2PChat

## Prerequisites
- Python 3
- grpc (Install with ``python3 -m pip install -r requirements.txt``)
- tkinter

## Preparation

Generate files with ``python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. passing.proto``

## Usage

Run with ``python main.py <ip> <port1> <port2>``.  
Example: ``python3 main.py localhost 6062 6061``.

# Made by
- Кутленков Дмитрий  
- Чернявский Олег
- Келим Илья
- Сергеев Егор

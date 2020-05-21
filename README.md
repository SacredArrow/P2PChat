# P2PChat

## Prerequisites
- Python 3
- grpc
- tkinter

## Preparation

Generate files with ``python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. passing.proto``

## Usage

Run with ``python main.py <ip> <port1> <port2>``.  
Example: ``python3 main.py localhost 6062 6061``.

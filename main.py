from bus import MessageBus
from server import Server
from interface import UserInterface
import sys


if __name__ == '__main__':
    port1, ip, port2 = sys.argv[1:4]
    bus = MessageBus()
    server = Server(bus)
    app = UserInterface(bus)
    server.start(ip, port1, port2)
    app.show()

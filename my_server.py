from concurrent import futures
import grpc
import datahash_pb2
import datahash_pb2_grpc
import sys
from interface import UserInterface
from bus import MessageBus, MessageType, Message
from threading import Thread


class Server:
    app = None
    server = None

    class DataHashServicer(datahash_pb2_grpc.DataHashServicer):
        def __init__(self, outer_instance):
            self.server = outer_instance

        def receive_message(self, request, context):
            response = datahash_pb2.Text()
            msg = Message(request.data, MessageType.CLIENT_MESSAGE)
            self.server.pub.send_message(msg, "incoming")

            return response

    def __init__(self, publisher):
        self.pub = publisher
        self.pub.subscribe(self, ["outgoing", "client_closed"])

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))

        self.app = UserInterface(publisher)

        self.process = Thread(target=self.serve)
        self.process.start()

        self.app.show()

    def serve(self):
        port1, port2 = sys.argv[1:3]
        channel = grpc.insecure_channel('localhost:' + str(port2))

        stub = datahash_pb2_grpc.DataHashStub(channel)

        # прикреплям хандлеры
        datahash_pb2_grpc.add_DataHashServicer_to_server(
            self.DataHashServicer(self), self.server)

        # запускаемся на порту
        print('Starting server on port ' + str(port1))
        self.server.add_insecure_port('[::]:' + str(port1))
        self.server.start()

        while True:
            for msg in self.pub.get_messages(self):
                if msg.type == MessageType.CLIENT_CLOSED:
                    msg = Message("Server closed", MessageType.SERVER_CLOSED)
                    self.pub.send_message(msg, "server_closed")
                    exit(0)

                grpc_text = datahash_pb2.Text(data=msg.text)
                stub.receive_message(grpc_text)


if __name__ == '__main__':
    bus = MessageBus()
    server = Server(bus)
    server.serve()

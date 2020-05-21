from concurrent import futures
import grpc
import passing_pb2
import passing_pb2_grpc
import sys
from interface import UserInterface
from bus import MessageBus, MessageType, Message
from threading import Thread


class Server:
    server = None

    class PassingServicer(passing_pb2_grpc.PassingServicer):
        def __init__(self, outer_instance):
            self.server = outer_instance

        def receive_message(self, request, context):
            response = passing_pb2.Text()
            msg = Message(request.data, MessageType.CLIENT_MESSAGE)
            self.server.pub.send_message(msg, "incoming")
            return response

    def __init__(self, publisher):
        self.pub = publisher
        self.pub.subscribe(self, ["outgoing", "client_closed"])

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))

    def start(self, ip, port1, port2):
        # Windows-compatibility, otherwise use Process
        self.process = Thread(target=self.serve, args=[ip, port1, port2])
        self.process.start()

    def serve(self, ip, port1, port2):
        address = ip + ":" + str(port2)
        channel = grpc.insecure_channel(address)

        stub = passing_pb2_grpc.PassingStub(channel)

        # прикреплям хандлеры
        passing_pb2_grpc.add_PassingServicer_to_server(
            self.PassingServicer(self), self.server)

        # запускаемся на порту

        print('Starting server on port ' + str(port1))
        self.server.add_insecure_port('[::]:' + str(port1))
        self.server.start()
        running = True
        while running:
            for msg in self.pub.get_messages(self):
                if msg.type == MessageType.CLIENT_CLOSED:
                    msg = Message("Server closed", MessageType.SERVER_CLOSED)
                    self.pub.send_message(msg, "server_closed")
                    running = False
                else:
                    try:
                        grpc_text = passing_pb2.Text(data=msg.text)
                        stub.receive_message(grpc_text)
                    except grpc.RpcError as e:
                        if e.code() == grpc.StatusCode.UNAVAILABLE:
                            msg = Message("Peer cannot be reached",
                                          MessageType.CONNECTION_ERROR)
                            self.pub.send_message(msg, "incoming")

import time
from concurrent import futures
import grpc
import datahash
import datahash_pb2
import datahash_pb2_grpc
import sys
from interface import UserInterface
from multiprocessing import Process

class Server:
    app = None
    server = None

    class DataHashServicer(datahash_pb2_grpc.DataHashServicer):
        def __init__(self, outer_instance):
            self.server = outer_instance

        def receive_message(self, request, context):
            response = datahash_pb2.Text()
            self.server.app.insert_message(request.data)
            # response.data = datahash.receive_message(request.data)
            return response

    def __init__(self):
        # создаем сервер
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))

        self.app = UserInterface()

        self.process = Process(target=self.serve)
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
            while self.app.msg_q:
                msg = self.app.msg_q.get()
                print(msg)
                to_sha256 = datahash_pb2.Text(data=msg)
                response = stub.receive_message(to_sha256)


if __name__ == '__main__':
    server = Server()
    server.serve()

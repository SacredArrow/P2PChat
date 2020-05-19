import time
from concurrent import futures
import grpc
import datahash
import datahash_pb2
import datahash_pb2_grpc
import sys

class DataHashServicer(datahash_pb2_grpc.DataHashServicer):
    def receive_message(self, request, context):
        response = datahash_pb2.Text()
        response.data = datahash.receive_message(request.data)
        return response
def serve():
    # создаем сервер
    port1, port2 = sys.argv[1:3]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))

    channel = grpc.insecure_channel('localhost:' + str(port2))
    stub = datahash_pb2_grpc.DataHashStub(channel)

    # прикреплям хандлеры
    datahash_pb2_grpc.add_DataHashServicer_to_server(DataHashServicer(), server)
    # запускаемся на порту
    print('Starting server on port ' + str(port1))
    server.add_insecure_port('[::]:' + str(port1))
    server.start()

    while True:
      s = input()
      to_sha256 = datahash_pb2.Text(data=s)
      response = stub.receive_message(to_sha256)

if __name__ == '__main__':
    serve()

import grpc
import RemouteSmartRieltor_pb2_grpc
from concurrent import futures
import threading

from ClientService import ClientService
from EnginereService import EngineerService
from KeyRateParser import get_value_additional_feature



def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    RemouteSmartRieltor_pb2_grpc.add_ClientServiceServicer_to_server(ClientService(), server)
    RemouteSmartRieltor_pb2_grpc.add_EnginerServiceServicer_to_server(EngineerService(), server)
    server.add_insecure_port('localhost:15000')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    x = threading.Thread(target=get_value_additional_feature)
    x.start()
    server()
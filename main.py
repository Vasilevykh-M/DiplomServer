import grpc
import RemouteSmartRieltor_pb2_grpc
from concurrent import futures

from Services.ClientService import ClientService
from Services.EngineerService import EngineerService
from Models.ModelEngineerTorchNN import ModelServerTorchNN
from Models.ModelEngineerCatBoost import ModelServerCatBoost
from Models.ModelEngineerTorchNN import Model_NN

models = {
    "torch": ModelServerTorchNN("torch", Model_NN(None), False),
    "catboost": ModelServerCatBoost("catboost", 0, False),
    "stat": {}
}

def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    RemouteSmartRieltor_pb2_grpc.add_ClientServiceServicer_to_server(ClientService(models), server)
    RemouteSmartRieltor_pb2_grpc.add_EngineerServiceServicer_to_server(EngineerService(models), server)
    server.add_insecure_port('localhost:15000')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    server()
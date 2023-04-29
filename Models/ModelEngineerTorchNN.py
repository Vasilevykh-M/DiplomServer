from Models.Model import ModelServer
import torch.nn as nn
import torch


class Model_NN(nn.Module):
    def __init__(self, layer):
        super(Model_NN, self).__init__()
        self.layer = layer

    def forward(self, X):
        return self.layer(X)


class ModelServerTorchNN(ModelServer):
    def __init__(self, type, model_architecture, main):
        super(ModelServerTorchNN, self).__init__(type, model_architecture, main)
        self.model = Model_NN(model_architecture)

    def predict(self, X):
        super(ModelServerTorchNN, self).predict(X)
        X = torch.FloatTensor(X)
        return self.model(X)

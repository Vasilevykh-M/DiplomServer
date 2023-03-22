import torch
from catboost import CatBoostClassifier


class TheModelTorch(torch.nn.Module):
    def __init__(self):
        super(TheModelTorch, self).__init__()
        self.l1 = torch.nn.Linear(49, 80)
        self.r1 = torch.nn.ReLU()
        self.d1 = torch.nn.Dropout()
        self.l2 = torch.nn.Linear(80, 20)
        self.r2 = torch.nn.ReLU()
        self.d2 = torch.nn.Dropout()
        self.l3 = torch.nn.Linear(20, 2)

    def forward(self, X):
        layer = self.d1(self.r1(self.l1(X)))
        layer = self.d2(self.r2(self.l2(layer)))
        layer = self.l3(layer)
        return layer


class ModelServer:
    def __init__(self, type, model):
        self.type = type
        self.file_model = model
        self.model = None

    def load_model(self):
        if self.type == "torch":
            self.model = TheModelTorch()
            self.model.load_state_dict(torch.load(self.file_model))

        if self.type == "CatBoost":
            self.model = CatBoostClassifier()
            self.model.load_model(self.file_model)

    def predict(self, data):
        result = None
        if self.type == "torch":
            data = torch.tensor(data, dtype=torch.float32)
            result = self.predict_torch(data)

        if self.type == "CatBoost":
            result = self.predict_cat(data)

        return result

    def predict_torch(self, data):
        return "torch"

    def predict_cat(self, data):
        return "cat"

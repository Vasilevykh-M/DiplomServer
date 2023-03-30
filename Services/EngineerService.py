import collections
import io
import torch.nn

import RemouteSmartRieltor_pb2_grpc
import RemouteSmartRieltor_pb2
import pandas as pd

class EngineerService(RemouteSmartRieltor_pb2_grpc.EngineerService):

    def __init__(self, models):
        super(EngineerService, self).__init__()
        self.models = models

    def postTorchModel(self, TorchModel, context):
        layers = TorchModel.layers
        self.models["torch"].model.layer = torch.nn.Sequential()
        for i in layers:
            self.models["torch"].model.layer.append(torch.nn.Linear(layers[i].input, layers[i].output))
            if layers[i].dropout:
                self.models["torch"].model.layer.append(torch.nn.Dropout())
            self.models["torch"].model.layer.append(torch.nn.ReLU())
        self.models["torch"].model.load_state_dict(torch.load(io.BytesIO(TorchModel.weights)))
        return RemouteSmartRieltor_pb2.Response(code=1)

    def postCatBoostModel(self, CatBoostModel, context):
        with open("cat_boost.cbm", "wb") as f:
            f.write(CatBoostModel.weights)
        self.models["catboost"].model.load_model("cat_boost.cbm")
        return RemouteSmartRieltor_pb2.Response(code=1)

    def postStat(self, Stat, context):
        return RemouteSmartRieltor_pb2.Response(code=1)

    def getData(self, interval_data, context):
        return RemouteSmartRieltor_pb2.File(file=b"a")

    def postData(self,  file, context):
        return RemouteSmartRieltor_pb2.Response(code = 1)
from Models.Model import ModelServer
from catboost import CatBoostClassifier

class ModelServerCatBoost(ModelServer):
    def __init__(self, type, depth, main):
        self.model = CatBoostClassifier(depth = depth)
        super(ModelServerCatBoost, self).__init__(type, self.model, main)
        self.depth = depth

    def predict(self, X):
        super(ModelServerCatBoost, self).predict(X)
        Y = self.model.predict(data=X)
        return Y


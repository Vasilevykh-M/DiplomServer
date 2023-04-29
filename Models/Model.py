class ModelServer:
    def __init__(self, type, model_architecture, main):
        self.type = type
        self.model_architecture = model_architecture
        self.main = main

    def predict(self, X):
        return

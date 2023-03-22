class Feature:
    def __init__(self, name, count):
        self.name = name
        self.count = count


class FeatureCat(Feature):
    def __init__(self, name, count, values, assignment):
        super(FeatureCat, self).__init__(name, count)
        self.values = values
        self.distribution = assignment


class FeatureNum(Feature):
    def __init__(self, name, count, std, mean):
        super(FeatureNum, self).__init__(name, count)
        self.std = std
        self.mean = mean


class DataSet:
    def __init__(self, data, features):
        self.data = data
        self.features = features
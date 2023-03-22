import pandas as pd

import UserModule

import RemouteSmartRieltor_pb2_grpc
import RemouteSmartRieltor_pb2

class ClientService(RemouteSmartRieltor_pb2_grpc.ClientService):

    def postData(self, file, context):
        parsed = pd.read_excel(file.file)
        UserModule.post_value_feature(parsed)
        return RemouteSmartRieltor_pb2.Response(code = 1)

    def getPredict(self, file, context):
        parsed = pd.read_excel(file.file)
        return RemouteSmartRieltor_pb2.Predict(predict =b'a')
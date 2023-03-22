import RemouteSmartRieltor_pb2_grpc
import RemouteSmartRieltor_pb2

import pandas as pd

import UserModule


class EngineerService(RemouteSmartRieltor_pb2_grpc.EnginerService):
    def postModel(self, file, context):
        return RemouteSmartRieltor_pb2.Response(code=1)

    def postStat(self, Stat, context):
        return RemouteSmartRieltor_pb2.Response(code=1)

    def getData(self, interval_data, context):
        return RemouteSmartRieltor_pb2.File(file=b"a")

    def postData(self,  file, context):
        parsed = pd.read_excel(file.file)
        UserModule.post_value_feature(parsed)
        return RemouteSmartRieltor_pb2.Response(code = 1)
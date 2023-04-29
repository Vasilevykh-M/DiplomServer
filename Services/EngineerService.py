import io
import torch.nn
import psycopg2
from datetime import datetime

import RemouteSmartRieltor_pb2_grpc
import RemouteSmartRieltor_pb2


from DataSet import DataSet

class EngineerService(RemouteSmartRieltor_pb2_grpc.EngineerService):

    def __init__(self, models):
        super(EngineerService, self).__init__()
        self.models = models

    def postTorchModel(self, TorchModel, context):
        layers = TorchModel.layers
        self.models["torch"].model.layer = torch.nn.Sequential()
        layers = dict(sorted(layers.items()))
        for i in layers:
            self.models["torch"].model.layer.append(torch.nn.Linear(layers[i].input, layers[i].output))
            print(i, layers[i].input, layers[i].output)
            if layers[i].dropout:
                self.models["torch"].model.layer.append(torch.nn.Dropout())
            self.models["torch"].model.layer.append(torch.nn.ReLU())
        self.models["torch"].model.load_state_dict(torch.load(io.BytesIO(TorchModel.weights)), strict=False)
        self.models["torch"].main = True
        self.models["catboost"].main = False
        return RemouteSmartRieltor_pb2.Response(code=1)

    def postCatBoostModel(self, CatBoostModel, context):
        with open("cat_boost.cbm", "wb") as f:
            f.write(CatBoostModel.weights)
        self.models["catboost"].model.load_model("cat_boost.cbm")
        self.models["torch"].main = False
        self.models["catboost"].main = True
        return RemouteSmartRieltor_pb2.Response(code=1)

    def postStat(self, Stat, context):
        for i in Stat.Stat:
            self.models['stat'][i] = DataSet.Feature(i, Stat.Stat[i].std, Stat.Stat[i].mean)
        return RemouteSmartRieltor_pb2.Response(code=1)

    def calc_quarter(self, month, year):
        m = month
        if m < 4:
            return '"ДатаБрони" >= ' + f"'{str(year)}.01.01'" + 'and "ДатаБрони" < ' + f"'{str(year)}.04.01'"
        if m >= 4 and m < 7:
            return '"ДатаБрони" >= ' + f"'{str(year)}.04.01'" + 'and "ДатаБрони" < ' + f"'{str(year)}.07.01'"
        if m >= 7 and m < 10:
            return '"ДатаБрони" >= ' + f"'{str(year)}.07.01'" + 'and "ДатаБрони" < ' + f"'{str(year)}.10.01'"
        if m > 10:
            return '"ДатаБрони" >= ' + f"'{str(year)}.10.01'" + 'and "ДатаБрони" < ' + f"'{str(year+1)}.01.01'"

    def create_genereator_to_post(self, df):
        for data in df:
            yield RemouteSmartRieltor_pb2.TrainData(Data=
                RemouteSmartRieltor_pb2.Data(
                Booking=RemouteSmartRieltor_pb2.Booking(
                    BookingDate=str(data[0]),
                    BookingTime=str(data[1]),
                    BookingSource=data[2],
                    BookingTemporary=data[3],
                    City=data[5],
                    TypeRoom=data[6],
                    TypeObject=data[7],
                    Area=int(data[8]),
                    Floor=int(data[9]),
                    Cost=int(data[10]),
                    TypeCost=data[11],
                    PaymentOption=data[12],
                    PaymentOptionAdditional=data[13],
                    Discount=int(data[14]),
                    ActualCost=int(data[15]),
                    DealAN=data[16],
                    InvestmentProduct=data[17],
                    Privilege=data[18],
                    LeadStatus=data[19],
                ),
                StateBooking=RemouteSmartRieltor_pb2.StateBooking(StateBooking=data[4])
            ),
            KeyRate=data[21]
            )

    def getData(self, responce, context):
        cur_date = datetime.now().date()
        cur_year = cur_date.year
        result = []

        with psycopg2.connect(database="talan", user="postgres", password="postgres",
                              host="localhost", port=5432) as conn:
            cur = conn.cursor()
            request = 'SELECT *\
                        FROM feature JOIN additional_feature ON feature."ДатаБрони" = additional_feature.date_rate\
                        WHERE "ДатаБрони" >= ' + f"'{str(cur_year - 1)}.01.01'" + 'and "ДатаБрони" <= '+f"'{str(cur_date)}'"
            cur.execute(request)
            result = cur.fetchall()

            request = f'SELECT *\
                        FROM feature JOIN additional_feature ON feature."ДатаБрони" = additional_feature.date_rate\
                        WHERE {self.calc_quarter(cur_date.month, cur_date.year - 2)} \
                        ORDER BY random()\
                        LIMIT 500;'
            cur.execute(request)
            result = result + cur.fetchall()
        print(result)
        return self.create_genereator_to_post(result)

    def postData(self, Data, context):

        with psycopg2.connect(database="talan", user="postgres", password="postgres",
                              host="localhost", port=5432) as conn:
            cur = conn.cursor()
            for row in Data:
                req = "INSERT INTO feature VALUES (" + \
                      f"'{row.Booking.BookingDate}'" + ", " + f"'{row.Booking.BookingTime}'" + ", " + f"'{row.Booking.BookingSource}'" + ", " + \
                      f"'{row.Booking.BookingTemporary}'" + ", " + f"'{row.StateBooking.StateBooking}'" + ", " + f"'{row.Booking.City}'" + ", " + \
                      f"'{row.Booking.TypeRoom}'" + ", " + f"'{row.Booking.TypeObject}'" + ", " + str(
                    row.Booking.Area) + ", " + \
                      str(row.Booking.Floor) + ", " + str(
                    row.Booking.Cost) + ", " + f"'{row.Booking.TypeCost}'" + ", " + \
                      f"'{row.Booking.PaymentOption}'" + ", " + f"'{row.Booking.PaymentOptionAdditional}'" + ", " + str(
                    row.Booking.Discount) + ", " + \
                      str(row.Booking.ActualCost) + ", " + f"'{row.Booking.DealAN}'" + ", " + f"'{row.Booking.InvestmentProduct}'" + ", " + \
                      f"'{row.Booking.Privilege}'" + ", " + f"'{row.Booking.LeadStatus}'" + ")"
                cur.execute(req)
            conn.commit()

        return RemouteSmartRieltor_pb2.Response(code = 1)
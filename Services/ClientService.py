from datetime import datetime

import pandas as pd
import psycopg2
import torch

import RemouteSmartRieltor_pb2_grpc
import RemouteSmartRieltor_pb2
from DataSet import DataSet


class ClientService(RemouteSmartRieltor_pb2_grpc.ClientService):

    def __init__(self, models):
        super(ClientService, self).__init__()
        self.models = models

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

    def convert_data(self, Y):
        for i in Y:
            yield RemouteSmartRieltor_pb2.StateBooking(StateBooking="Выйдет" if i != 0 else "Не выйдет")

    def getPredict(self, Booking, context):

        data = {
            "ДатаБрони": [],
            "ВремяБрони": [],
            "ДеньНедели": [],
            "ИсточникБрони": [],
            "ВременнаяБронь": [],
            "Город": [],
            "ВидПомещения": [],
            "Тип": [],
            "ПродаваемаяПлощадь": [],
            "Этаж": [],
            "СтоимостьНаДатуБрони": [],
            "ТипСтоимости": [],
            "ВариантОплаты": [],
            "ВариантОплатыДоп": [],
            "СкидкаНаКвартиру": [],
            "Скидка%": [],
            "ФактическаяСтоимостьПомещения": [],
            "СделкаАН": [],
            "ИнвестиционныйПродукт": [],
            "Привилегия": [],
            "Статус лида (из CRM)": [],
            "ЦенаЗаКвМетр": []
        }
        for i in Booking:
            data["ДатаБрони"].append(datetime.strptime(i.BookingDate, "%Y-%m-%d %H:%M:%S").month)
            data["ВремяБрони"].append(datetime.strptime(i.BookingTime, "%H:%M:%S").hour)
            data["ДеньНедели"].append(datetime.strptime(i.BookingDate, "%Y-%m-%d %H:%M:%S").weekday())
            data["ИсточникБрони"].append(i.BookingSource)
            data["ВременнаяБронь"].append(i.BookingTemporary)
            data["Город"].append(i.City)
            data["ВидПомещения"].append(i.TypeRoom)
            data["Тип"].append(i.TypeObject)
            data["ПродаваемаяПлощадь"].append(i.Area)
            data["Этаж"].append(i.Floor)
            data["СтоимостьНаДатуБрони"].append(i.Cost)
            data["ТипСтоимости"].append(i.TypeCost)
            data["ВариантОплаты"].append(i.PaymentOption)
            data["ВариантОплатыДоп"].append(i.PaymentOptionAdditional)
            data["СкидкаНаКвартиру"].append(i.Discount)
            data["Скидка%"].append(i.ActualCost / i.Discount if i.Discount != 0 else 0.0)
            data["ФактическаяСтоимостьПомещения"].append(i.ActualCost)
            data["СделкаАН"].append(i.DealAN)
            data["ИнвестиционныйПродукт"].append(i.InvestmentProduct)
            data["Привилегия"].append(i.Privilege)
            data["Статус лида (из CRM)"].append(i.LeadStatus)
            data["ЦенаЗаКвМетр"].append(i.ActualCost / i.Area)
        df = pd.DataFrame.from_dict(data)

        dataset = DataSet.DataSet(df, self.models["stat"])
        dataset.pre_data()

        X = dataset.data
        X = X.to_numpy()

        Y = [0]

        if self.models["torch"].main:
            Y = torch.max(self.models["torch"].predict(X), 1).indices
        if self.models["catboost"].main:
            Y = self.models["catboost"].predict(X)

        return self.convert_data(Y)
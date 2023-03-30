import psycopg2

import RemouteSmartRieltor_pb2_grpc
import RemouteSmartRieltor_pb2

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

    def getPredict(self, Booking, context):
        return RemouteSmartRieltor_pb2.Predict(predict =b'a')
import zeep
import time
from datetime import datetime
from datetime import date
import psycopg2



# сделать запрос к ЦБ и получить значения
def get_value_additional_feature():
    while True:
        while True:
            try:
                client = zeep.client.Client('https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL')
                break
            except:
                print("Error connect!!!")
                time.sleep(30)
        today = date.today()
        root = client.service.KeyRateXML(today, today)
        for i in root:
            print((i.findtext("DT")[:10], i.findtext("Rate")))
            post_value_additional_feature((i.findtext("DT")[:10], i.findtext("Rate")))
        client.transport.session.close()
        time.sleep(86400)


# отправить значения в БД
def post_value_additional_feature(value):
    with psycopg2.connect(database="talan", user="postgres", password="postgres",
                          host="localhost", port=5432) as conn:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO additional_feature VALUES ('{datetime.strptime(value[0], '%Y-%m-%d').date()}', {value[1]})")
        conn.commit()
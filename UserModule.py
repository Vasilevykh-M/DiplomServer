import psycopg2
import openpyxl

import datetime
import pandas as pd
import numpy as np




# кодирование категорилаьных признаков
def encoding_data(data):
    list_cat_data = ["ИсточникБрони", "ВременнаяБронь", "ТипСтоимости", "ВариантОплаты",
                     "ВариантОплатыДоп", "СделкаАН", "ИнвестиционныйПродукт", "Привилегия"]
    for i in list_cat_data:
        data[i] = data[i].astype('category')
        data[i] = data[i].cat.codes
        data.drop(columns=[i], axis=1, inplace=True)
    return data


# предобработка данных
def preprocessing_data(data, dict_stat):
    data = encoding_data(data)

    dict_city={}
    cities = set(pd.Series(data["Город"]))
    for i in cities:
        dict_city[i] = hash(i) % 20

    for i in dict_city:
        data["Город"] = data["Город"].replace(i, dict_stat[i])
    for feature in dict_stat:
        data[feature] = (data[feature] - dict_stat[feature]["mean"])/dict_stat[feature]["std"]

    data = pd.get_dummies(data, columns=['ВидПомещения', 'Тип', 'Статус лида (из CRM)'])

    data['ДатаБрони'] = data['ДатаБрони'].dt.strftime('%m').astype('int')

    t = np.zeros(len(data.index))
    j = 0
    for i in data['ВремяБрони']:
        t[j] = i.hour
        j += 1
    data['ВремяБрони'] = t
    return data


# отправить данные в БД
def post_value_feature(arr):
    dict_columns = {
        "ДатаБрони": [],
        "ВремяБрони": [],
        "ИсточникБрони": [],
        "ВременнаяБронь": [],
        "СледующийСтатус": [],
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
        "ФактическаяСтоимостьПомещения": [],
        "СделкаАН": [],
        "ИнвестиционныйПродукт": [],
        "Привилегия": [],
        "Статус лида (из CRM)": []
    }


    with psycopg2.connect(database="talan", user="postgres", password="postgres",
                          host="localhost", port=5432) as conn:
        cur = conn.cursor()
        for col_name, data in arr.items():
            if col_name in dict_columns:
                for i in range(len(data)):
                    dict_columns[col_name].append(f"'{data[i]}'" if isinstance(data[i], str) or isinstance(data[i], datetime.datetime) or isinstance(data[i], datetime.time) else str(data[i]))
        for i in range(len(arr)):
            body_request =""
            for j in dict_columns:
                print(j + " " + dict_columns[j][i])
                body_request += dict_columns[j][i] + (', ' if j != "Статус лида (из CRM)" else "")
            print(body_request)
            cur.execute(f"INSERT INTO feature VALUES({body_request})")
        conn.commit()

# получить дополнительные параметры
def get_additional_feature(data):

    str = ""
    for i in set(pd.Series(data["ДатаБрони"])):
        str += i + ", "

    str=str[:-2] + ")"


    with psycopg2.connect(database="talan", user="postgres", password="postgres",
                          host="localhost", port=5432) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM additional_feature WHERE date_rate in ({str})")
        rows = cur.fetchall()
        return rows

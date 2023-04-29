class Feature:
    def __init__(self, name, std, mean):
        self.name = name
        self.std = std
        self.mean = mean


class DataSet:
    def __init__(self, data, feature):
        self.data = data
        self.feature = feature

    def clean_missing_values(self):
        self.data = self.data.fillna(
            value={
                'Этаж':0,
                'СкидкаНаКвартиру': 0,
                'СледующийСтатус': 'В резерве',
                'ВариантОплатыДоп': 'нет'
            }
        )

    def normalization(self, list_feature):
        for i in list_feature:
            self.data[i] = (self.data[i] - self.feature[i].mean) / self.feature[i].std

    def cat_features(self, list_feature):
        for i in list_feature:
            self.data[i] = self.data[i].astype('category')
            self.data[i] = self.data[i].cat.codes
            self.data.drop(columns=[i], axis=1, inplace=True)

    def hash_codes(self, list_feature):
        for i in list_feature:
            self.data[i] = self.data[i].map(lambda x: hash(x)%100)

    def pre_data(self):
        self.cat_features([
            "ИсточникБрони", "ВременнаяБронь",
            "ТипСтоимости", "ВариантОплаты",
            "ВариантОплатыДоп", "СделкаАН",
            "ИнвестиционныйПродукт", "Привилегия",
        ])
        self.hash_codes(["Город", "Статус лида (из CRM)", "ВидПомещения", "Тип"])
        self.normalization([
            'ДатаБрони', 'ПродаваемаяПлощадь', 'Этаж',
            'СтоимостьНаДатуБрони', 'ФактическаяСтоимостьПомещения', 'ЦенаЗаКвМетр',
            'ВремяБрони', 'СкидкаНаКвартиру', 'Город',
            'Статус лида (из CRM)', 'ВидПомещения', 'Тип',
            'Скидка%'
        ])
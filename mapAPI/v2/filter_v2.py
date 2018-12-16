# -*- coding: utf-8 -*-
from pandas import Series
import numpy as np


class JibunFilter:
    """
        This class transforms from raw jibun address to jibun address.
    """
    def __call__(self, data):
        # Data Type Check
        if not isinstance(data, (Series, list, str)):
            raise TypeError

        # From raw data to list type data
        if isinstance(data, str):
            address = [data]
        else:
            address = [d for d in data]

        # Main Process Part
        result = list()
        for addr in address:
            try:
                tmp = addr.split(" ")
            except AttributeError:
                result.append("입력주소없음")
                continue

            idx = None
            for i, t in enumerate(tmp):
                if t[-2:] == '번지':
                    idx = i + 1
                    break
            tmp = tmp[0:idx]

            element = {'do': "", 'si': "", 'gu': "", 'dong': "", 'bunji': ""}
            if tmp[0][-1:] == '시':
                element['si'] = tmp[0]
                for t in tmp[1:]:
                    if t[-1:] == '구' or t[-1:] == '군':
                        element['gu'] = t
                    elif t[-1:] == '읍' or t[-1:] == '면' or t[-1:] == '동' or t[-1:] == '가' or t[-1:] == '로':
                        element['dong'] = t
                    elif t[-2:] == '번지':
                        bunji = t[:-2].split('-')
                        if len(bunji) == 2 and bunji[1] == '0':
                            element['bunji'] = bunji[0]
                        else:
                            element['bunji'] = t[:-2]
                    else:
                        continue
                if element['si'] != "" and element['gu'] != "" and element['dong'] != "" and element['bunji'] != "":
                    result.append(" ".join(list(element.values())))
                else:
                    result.append('입력주소오류')
            elif tmp[0][-1:] == '도':
                element['do'] = tmp[0]
                for t in tmp[1:]:
                    if t[-1:] == '시' or t[-1:] == '군':
                        element['si'] = t
                    elif t[-1:] == '구':
                        element['gu'] = t
                    elif t[-1:] == '읍' or t[-1:] == '면' or t[-1:] == '동':
                        element['dong'] = t
                    elif t[-2:] == '번지':
                        bunji = t[:-2].split('-')
                        if len(bunji) == 2 and bunji[1] == '0':
                            element['bunji'] = bunji[0]
                        else:
                            element['bunji'] = t[:-2]
                    else:
                        continue
                if element['do'] != "" and element['si'] != "" and element['gu'] == "" and element['dong'] != "" and \
                        element['bunji'] != "":
                    del element['gu']
                    result.append(" ".join(list(element.values())))
                elif element['do'] != "" and element['si'] != "" and element['gu'] != "" and element['dong'] != "" and \
                        element['bunji'] != "":
                    result.append(" ".join(list(element.values())))
                else:
                    result.append('입력주소오류')
            else:
                result.append("입력주소오류")

        return np.array(result)


if __name__ == '__main__':
    pass
